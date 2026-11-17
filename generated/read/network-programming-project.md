PROJECT · NETWORK PROGRAMMING IN C++

# Sockets from scratch a chat server and an HTTP server

A small, complete C++ project that turns networking theory into code you wrote: a poll()-based multi-client chat server and a minimal HTTP/1.1 server, with tests over real sockets. Each page explains what the code shows and what to say about it in an interview.

| Section                                                 |
|---------------------------------------------------------|
| [1. What you build and why](#01-what-you-build-and-why)                    |
| [2. The system calls, in order](#02-the-system-calls-in-order)                |
| [3. TCP is a byte stream: framing](#03-tcp-is-a-byte-stream-framing)             |
| [4. What the HTTP server shows](#04-what-the-http-server-shows)                |
| [5. Interview questions this prepares you for](#05-interview-questions-this-prepares-you-for) |
| [6. Extend it and put it on your resume](#06-extend-it-and-put-it-on-your-resume)       |
| [Sources (1)](#-sources)                                  |

Code: `generated/netproj/` (chat_server.cpp, http_server.cpp, test_net.py). All 11 socket tests pass under AddressSanitizer and UndefinedBehaviorSanitizer.

## 01. What you build and why

- **chat_server.cpp:** one thread serves many clients with `poll()`; each line a client sends goes to every other client. About 70 lines.
- **http_server.cpp:** a minimal HTTP/1.1 server with `GET /` and `GET /hello?name=…`, and 404, 405 and 400 for everything else. The request handling is a pure function, so it is easy to test.
- **test_net.py:** builds both with AddressSanitizer, starts them on free localhost ports and checks 11 behaviours over real sockets, including a line split across two TCP sends.
- **Why:** networking questions ("what happens when you type a URL", "TCP vs UDP", "how does a server handle many clients") come up in almost every SDE and security interview. Having written the syscalls yourself makes the answers concrete. It is also a solid small C++ project for your resume.

### Build and run (Linux, macOS or WSL)

``` bash
cd generated/netproj
g++ -std=c++17 -Wall -Wextra -O2 chat_server.cpp -o chat_server && ./chat_server 9000
nc 127.0.0.1 9000          # in two more terminals; type lines in each
g++ -std=c++17 -Wall -Wextra -O2 http_server.cpp -o http_server && ./http_server 8080
curl -i "127.0.0.1:8080/hello?name=Asha"
python3 test_net.py        # 11 checks
```

## 02. The system calls, in order

| Call                                                                               | What it does                                                      | What to say in an interview                                                        |
|------------------------------------------------------------------------------------|-------------------------------------------------------------------|------------------------------------------------------------------------------------|
| [socket](https://man7.org/linux/man-pages/man2/socket.2.html)                      | Creates an endpoint; returns a file descriptor                    | Everything in Unix is a file descriptor; AF_INET + SOCK_STREAM means TCP over IPv4 |
| [setsockopt](https://man7.org/linux/man-pages/man2/setsockopt.2.html) SO_REUSEADDR | Lets the server bind again while old connections sit in TIME_WAIT | Without it a quick restart fails with 'Address already in use'                     |
| [bind](https://man7.org/linux/man-pages/man2/bind.2.html)                          | Attaches the socket to an address and port                        | 127.0.0.1 = this machine only; 0.0.0.0 = every interface (exposed)                 |
| [listen](https://man7.org/linux/man-pages/man2/listen.2.html)                      | Marks it as a server socket with a backlog queue                  | The kernel completes handshakes and queues them before accept                      |
| [accept](https://man7.org/linux/man-pages/man2/accept.2.html)                      | Takes one finished connection; returns a new fd for it            | The listening fd stays open; one fd per client                                     |
| [poll](https://man7.org/linux/man-pages/man2/poll.2.html)                          | Waits until any of many fds is readable                           | One thread, many clients; epoll scales better for thousands                        |
| [recv](https://man7.org/linux/man-pages/man2/recv.2.html)                          | Reads available bytes; 0 means the peer closed                    | It returns whatever has arrived, not a whole message                               |
| [send](https://man7.org/linux/man-pages/man2/send.2.html)                          | Writes bytes; may write fewer than asked                          | Loop until all are sent; MSG_NOSIGNAL avoids SIGPIPE on a closed peer              |
| [close](https://man7.org/linux/man-pages/man2/close.2.html)                        | Releases the fd; TCP sends FIN                                    | The side that closes first goes to TIME_WAIT                                       |

## 03. TCP is a byte stream: framing

TCP keeps the order of bytes but not your message boundaries. One `send` of 20 bytes can arrive as two `recv`s of 10, and two sends can arrive as one. The chat server therefore keeps a buffer per client and only acts on complete lines; the test sends half a line, waits, then sends the rest, and checks it arrives whole.

``` cpp
std::string& b = inbuf[fd]; b.append(buf, n);          // keep what arrived
size_t nl;
while ((nl = b.find('\n')) != std::string::npos) {   // act only on complete lines
    std::string line = ... b.substr(0, nl + 1); b.erase(0, nl + 1);
    for (auto& p : fds) if (p.fd != lfd && p.fd != fd) send_all(p.fd, line);
}
```

- Other framings: a length prefix (binary protocols), or a delimiter (HTTP headers end with a blank line, \r\n\r\n).
- send() can also be partial: send_all() loops until everything is written.

## 04. What the HTTP server shows

- A request is a request line (`GET /path HTTP/1.1`), headers, a blank line, then an optional body. The server reads until \r\n\r\n.^([\[1\]](#-sources))
- The response needs a status line, Content-Length (or chunked encoding) and the blank line; `Connection: close` keeps it one request per connection.
- 405 must include an `Allow` header; 400 is for requests that cannot be parsed.
- Security points you can mention: the server binds to 127.0.0.1 only, caps the header size at 8 KB, and never trusts the path (no file serving, so no path traversal). A real server would also add timeouts against slow clients (Slowloris).

## 05. Interview questions this prepares you for

| Question                                   | Short answer                                                                                                                                |
|--------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| How does one thread serve many clients?    | I/O multiplexing: poll/epoll waits on all sockets and the loop handles whichever are ready; no thread per client.                           |
| poll vs epoll?                             | poll passes the whole list every call (O(n)); epoll keeps the set in the kernel and returns only ready fds, so it scales to many thousands. |
| What does recv returning 0 mean?           | The peer closed its side cleanly (FIN). Negative means an error.                                                                            |
| Why can send write fewer bytes than asked? | The kernel send buffer is full; loop, or use non-blocking sockets and wait for POLLOUT.                                                     |
| What is TIME_WAIT and why SO_REUSEADDR?    | The side that closes first waits 2 × MSL so late packets die; SO_REUSEADDR lets a server rebind meanwhile.                                  |
| Threads vs event loop?                     | Threads are simple but cost memory and context switches; an event loop is cheap per connection but every handler must be non-blocking.      |
| What happens when you type a URL?          | DNS lookup, TCP handshake, TLS handshake, HTTP request, server work, response, rendering. Your server implements the HTTP step.             |

## 06. Extend it and put it on your resume

- Non-blocking sockets and epoll; a thread pool for the HTTP server; keep-alive; serving files safely (realpath and a base-directory check).
- Usernames and /commands in the chat; a load test (many clients) with timings.
- Resume line: "Built a single-threaded poll()-based chat server and an HTTP/1.1 server in C++17, with framing and partial-send handling, tested over real sockets under AddressSanitizer."
- Related: [Linux and debugging sheet](linux-git-debugging-sheet.md), [security labs (packet capture)](security-labs-workbook.md).

## ··. Sources

Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.

1.  [RFC 9112: HTTP/1.1 message syntax](https://www.rfc-editor.org/rfc/rfc9112)  
    https://www.rfc-editor.org/rfc/rfc9112
