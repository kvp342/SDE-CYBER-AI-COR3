// Minimal HTTP/1.1 server: GET / and GET /hello?name=X; 404, 405 and 400 otherwise; one request per connection.
// Build: g++ -std=c++17 -Wall -Wextra -O2 http_server.cpp -o http_server   Run: ./http_server 8080   Try: curl -i 127.0.0.1:8080/hello?name=Asha
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#include <cerrno>
#include <cstdio>
#include <cstdlib>
#include <string>

static std::string response(int code, const std::string& reason, const std::string& body, const std::string& extra = "") {
    return "HTTP/1.1 " + std::to_string(code) + " " + reason + "\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " +
           std::to_string(body.size()) + "\r\nConnection: close\r\n" + extra + "\r\n" + body;
}
static std::string url_decode(const std::string& s) {
    std::string r;
    for (size_t i = 0; i < s.size(); i++) {
        if (s[i] == '+') r += ' ';
        else if (s[i] == '%' && i + 2 < s.size() && isxdigit((unsigned char)s[i + 1]) && isxdigit((unsigned char)s[i + 2])) { r += (char)std::stoi(s.substr(i + 1, 2), nullptr, 16); i += 2; }
        else r += s[i];
    }
    return r;
}
std::string handle(const std::string& req) {                     // pure function: easy to test
    size_t eol = req.find("\r\n");
    if (eol == std::string::npos) return response(400, "Bad Request", "bad request\n");
    std::string line = req.substr(0, eol); size_t s1 = line.find(' '), s2 = line.rfind(' ');
    if (s1 == std::string::npos || s2 == s1 || line.compare(s2 + 1, 5, "HTTP/") != 0) return response(400, "Bad Request", "bad request\n");
    std::string method = line.substr(0, s1), target = line.substr(s1 + 1, s2 - s1 - 1);
    if (method != "GET") return response(405, "Method Not Allowed", "only GET\n", "Allow: GET\r\n");
    std::string path = target.substr(0, target.find('?')), query = target.find('?') == std::string::npos ? "" : target.substr(target.find('?') + 1);
    if (path == "/") return response(200, "OK", "hello from a tiny C++ server\n");
    if (path == "/hello") {
        std::string name = "guest"; size_t p = query.find("name=");
        if (p != std::string::npos) name = url_decode(query.substr(p + 5, query.find('&', p) - (p + 5)));
        return response(200, "OK", "Hello, " + name + "\n");
    }
    return response(404, "Not Found", "not found\n");
}

int main(int argc, char** argv) {
    int port = argc > 1 ? atoi(argv[1]) : 8080;
    int lfd = socket(AF_INET, SOCK_STREAM, 0); int yes = 1; setsockopt(lfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof yes);
    sockaddr_in a{}; a.sin_family = AF_INET; a.sin_port = htons(port); a.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(lfd, (sockaddr*)&a, sizeof a) < 0 || listen(lfd, 64) < 0) { perror("bind/listen"); return 1; }
    printf("listening on 127.0.0.1:%d\n", port); fflush(stdout);
    while (true) {
        int c = accept(lfd, nullptr, nullptr); if (c < 0) { if (errno == EINTR) continue; perror("accept"); return 1; }
        std::string req; char buf[2048];
        while (req.find("\r\n\r\n") == std::string::npos && req.size() < 8192) {   // read until the end of the headers
            ssize_t n = recv(c, buf, sizeof buf, 0); if (n <= 0) break; req.append(buf, n);
        }
        std::string out = handle(req); size_t off = 0;
        while (off < out.size()) { ssize_t n = send(c, out.data() + off, out.size() - off, MSG_NOSIGNAL); if (n <= 0) break; off += n; }
        close(c);
    }
}
