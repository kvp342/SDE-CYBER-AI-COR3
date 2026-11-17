#!/usr/bin/env bash
# Labs 1-3 as runnable steps. Run on YOUR OWN Linux machine or VM (WSL or a VirtualBox Ubuntu VM is fine).
# Needs: sudo apt install nmap tcpdump tshark curl openssl. Everything targets 127.0.0.1 only.
set -u
lab1() {   # file permissions and SUID (run as a normal user, not root: root ignores permissions)
  mkdir -p ~/lab1 && cd ~/lab1
  echo "secret notes" > notes.txt && chmod 640 notes.txt && ls -l notes.txt   # -rw-r----- : owner rw, group r, others nothing
  stat -c "%a %A" notes.txt                                                   # 640 -rw-r-----
  umask                                                                       # default mask for new files, often 0002 or 0022
  find /usr/bin -perm -4000 -type f                                           # SUID programs: run with their owner's rights
}
lab2() {   # scan only your own machine
  python3 -m http.server 8000 --bind 127.0.0.1 & srv=$!; sleep 1
  ss -tlnp | grep 8000                                                        # what is listening, from the inside
  nmap -sT -p 7990-8010 127.0.0.1                                             # from the outside: 8000 open, the rest closed
  nmap -sV -p 8000 127.0.0.1                                                  # version detection
  kill $srv
}
lab3() {   # see the difference between HTTP and HTTPS on the wire
  python3 -m http.server 8000 --bind 127.0.0.1 & srv=$!; sleep 1
  sudo tcpdump -i lo -w http.pcap -U port 8000 & cap=$!; sleep 1
  curl -s -o /dev/null "http://127.0.0.1:8000/?user=alice&password=hunter2"; sleep 1; sudo kill $cap; kill $srv
  tshark -r http.pcap -Y "tcp.flags.syn==1 || http.request" -T fields -e frame.number -e tcp.flags.str -e http.request.uri
  strings http.pcap | grep hunter2                                            # the password is readable
  openssl req -x509 -newkey rsa:2048 -nodes -keyout k.pem -out c.pem -days 1 -subj /CN=localhost
  openssl s_server -accept 8443 -cert c.pem -key k.pem -www -quiet & tls=$!; sleep 1
  sudo tcpdump -i lo -w tls.pcap -U port 8443 & cap=$!; sleep 1
  curl -sk -o /dev/null "https://127.0.0.1:8443/?user=alice&password=hunter2"; sleep 1; sudo kill $cap; kill $tls
  tshark -r tls.pcap -Y tls.handshake -T fields -e frame.number -e tls.handshake.type   # 1 = ClientHello, 2 = ServerHello
  strings tls.pcap | grep -c hunter2                                          # 0: the password is encrypted
}
"${1:-lab1}"
