// Multi-client chat server on one thread using poll(). Each line a client sends is broadcast to every other client.
// Build: g++ -std=c++17 -Wall -Wextra -O2 chat_server.cpp -o chat_server   Run: ./chat_server 9000   Try: nc 127.0.0.1 9000 (in two terminals)
#include <arpa/inet.h>
#include <netinet/in.h>
#include <poll.h>
#include <sys/socket.h>
#include <unistd.h>
#include <cerrno>
#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <string>
#include <vector>

static bool send_all(int fd, const std::string& s) {           // send() may write only part of the buffer
    size_t off = 0;
    while (off < s.size()) {
        ssize_t n = send(fd, s.data() + off, s.size() - off, MSG_NOSIGNAL);
        if (n < 0) { if (errno == EINTR) continue; return false; }
        off += (size_t)n;
    }
    return true;
}

int main(int argc, char** argv) {
    int port = argc > 1 ? atoi(argv[1]) : 9000;
    int lfd = socket(AF_INET, SOCK_STREAM, 0);
    if (lfd < 0) { perror("socket"); return 1; }
    int yes = 1; setsockopt(lfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof yes);   // allow quick restarts (TIME_WAIT)
    sockaddr_in a{}; a.sin_family = AF_INET; a.sin_port = htons(port); a.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(lfd, (sockaddr*)&a, sizeof a) < 0) { perror("bind"); return 1; }
    if (listen(lfd, 16) < 0) { perror("listen"); return 1; }
    printf("listening on 127.0.0.1:%d\n", port); fflush(stdout);
    std::vector<pollfd> fds{{lfd, POLLIN, 0}};
    std::map<int, std::string> inbuf;                            // TCP is a byte stream: keep partial lines per client
    while (true) {
        if (poll(fds.data(), fds.size(), -1) < 0) { if (errno == EINTR) continue; perror("poll"); return 1; }
        for (size_t i = 0; i < fds.size(); i++) {
            if (!(fds[i].revents & (POLLIN | POLLHUP | POLLERR))) continue;
            if (fds[i].fd == lfd) {                              // new connection
                int c = accept(lfd, nullptr, nullptr);
                if (c >= 0) { fds.push_back({c, POLLIN, 0}); inbuf[c]; send_all(c, "welcome\n"); }
                continue;
            }
            int fd = fds[i].fd; char buf[4096];
            ssize_t n = recv(fd, buf, sizeof buf, 0);
            if (n <= 0) {                                        // 0 = peer closed; <0 = error
                close(fd); inbuf.erase(fd); fds.erase(fds.begin() + i); i--;
                continue;
            }
            std::string& b = inbuf[fd]; b.append(buf, n);
            size_t nl;
            while ((nl = b.find('\n')) != std::string::npos) {   // broadcast each complete line
                std::string line = "user" + std::to_string(fd) + ": " + b.substr(0, nl + 1); b.erase(0, nl + 1);
                for (auto& p : fds) if (p.fd != lfd && p.fd != fd) send_all(p.fd, line);
            }
        }
    }
}
