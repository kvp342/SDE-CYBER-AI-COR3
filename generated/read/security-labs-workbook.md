SECURITY · HANDS-ON

# 6 security labs on your own machine

Six labs that turn the security theory in this kit into things you have done and can talk about: permissions and SUID, port scanning, packet capture of HTTP versus HTTPS, password hashing and cracking, finding and fixing SQL injection and XSS in a small app, and writing a brute-force detection rule. Each lab lists the steps, the output you should see (captured when the labs were tested on Linux), what to write in your lab notebook, and the defence.

**Legal and ethics: read first.** Do these labs only on machines you own, a VM you control, or platforms that invite you (TryHackMe, Hack The Box, PortSwigger Academy). Everything here targets 127.0.0.1. In India, accessing a computer without the owner's permission is penalised under Section 43 of the Information Technology Act, 2000, and doing it dishonestly or fraudulently is an offence under Section 66 (imprisonment up to three years) ([Council of Europe legal profile of India](https://rm.coe.int/octocom-legal-profile-india-rev/16809e8fe5)). Scanning a college or company network without written permission can end a security career before it starts.

| Lab                                                          |
|--------------------------------------------------------------|
| [Lab 1. Linux permissions and SUID](#lab-1-linux-permissions-and-suid)                 |
| [Lab 2. Port scanning your own machine](#lab-2-port-scanning-your-own-machine)             |
| [Lab 3. HTTP vs HTTPS on the wire](#lab-3-http-vs-https-on-the-wire)                  |
| [Lab 4. Hashing and cracking your own test hashes](#lab-4-hashing-and-cracking-your-own-test-hashes) |
| [Lab 5. Find and fix SQL injection and XSS](#lab-5-find-and-fix-sql-injection-and-xss)        |
| [Lab 6. Detect a brute-force attack in a log](#lab-6-detect-a-brute-force-attack-in-a-log)      |

**Code.** Everything is in `generated/security-labs/`: [app_vulnerable.py](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/security-labs/app_vulnerable.py) · [app_fixed.py](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/security-labs/app_fixed.py) · [detect_bruteforce.py](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/security-labs/detect_bruteforce.py) · [crack_lab.py](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/security-labs/crack_lab.py) · [cli_labs.sh](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/security-labs/cli_labs.sh) · [test_labs.py](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/security-labs/test_labs.py). `test_labs.py` (7 tests) proves each exploit works on the vulnerable app and fails on the fixed one. Use the security lab notebook template for write-ups, then publish clean versions on GitHub.

## LAB 1. Linux permissions and SUID

About 40 minutes

**Why.** Every privilege-escalation write-up starts here, and interviewers ask what chmod 750 means.

**Setup.** Any Linux machine, WSL or VM. Work as a normal user: root ignores permissions. Create a second user (sudo useradd -m other) to test access.

### Steps

``` bash
mkdir -m 777 /tmp/lab1 && cd /tmp/lab1
echo "secret notes" > notes.txt && chmod 640 notes.txt && ls -l notes.txt
sudo -u other cat /tmp/lab1/notes.txt        # denied: others have no read bit
chmod 644 notes.txt && sudo -u other cat notes.txt   # now readable
sudo -u other sh -c 'echo x >> /tmp/lab1/notes.txt'   # still no write bit
cp /usr/bin/id myid && chmod u+s myid && ls -l myid
sudo -u other ./myid -u     # runs with YOUR uid: that is SUID
find /usr/bin -perm -4000 -type f      # SUID programs on the system
```

### What you should see

``` text
-rw-r----- labuser  notes.txt
cat: /tmp/lab1/notes.txt: Permission denied
secret notes
sh: 1: cannot create /tmp/lab1/notes.txt: Permission denied
-rwsr-xr-x  myid
30033            <- labuser's uid, although 'other' ran it
/usr/bin/sudo  /usr/bin/passwd  /usr/bin/su  /usr/bin/mount ...
```

### Write in your lab notebook

- Permission string of each file before and after, and what each bit allowed or blocked.
- Which SUID programs exist and why each needs root (passwd edits /etc/shadow).
- One sentence: why a writable SUID root binary is a privilege-escalation hole.

**Defence.** Least privilege: no SUID on custom programs, umask 027 for sensitive users, audit SUID files regularly (find / -perm -4000).

## LAB 2. Port scanning your own machine

About 30 minutes

**Why.** Shows what 'open', 'closed' and 'filtered' mean, and how a service looks from inside versus outside.

**Setup.** sudo apt install nmap. Scan only 127.0.0.1 or a VM you own on a host-only network.

### Steps

``` bash
python3 -m http.server 8000 --bind 127.0.0.1 &
ss -tlnp | grep 8000             # inside view: who listens
nmap -sT -p 7990-8010 127.0.0.1   # outside view
nmap -sV -p 8000 127.0.0.1        # version detection
kill %1
```

### What you should see

``` text
LISTEN 0 5 127.0.0.1:8000 0.0.0.0:* users:(("python3",...))
PORT     STATE  SERVICE
7999/tcp closed irdmi2
8000/tcp open   http-alt
8001/tcp closed vcom-tunnel
...
8000/tcp open  http    SimpleHTTPServer 0.6 (Python 3.13)
```

### Write in your lab notebook

- The inside view (ss) and the outside view (nmap) side by side.
- Why closed ports answer at once (RST) but filtered ones time out (try with a firewall rule on a VM).
- What -sV revealed, and why version banners help attackers.

**Defence.** Bind services to 127.0.0.1 unless they must be public; close what you do not use; hide version banners; firewall by default-deny.

## LAB 3. HTTP vs HTTPS on the wire

About 45 minutes

**Why.** You will be asked what TLS protects. Seeing a password in a capture answers it for good.

**Setup.** sudo apt install tcpdump tshark curl openssl (or use Wireshark's GUI on the loopback interface).

### Steps

``` bash
python3 -m http.server 8000 --bind 127.0.0.1 &
sudo tcpdump -i lo -w http.pcap -U port 8000 &
curl -s "http://127.0.0.1:8000/?user=alice&password=hunter2" > /dev/null; sudo kill %2
tshark -r http.pcap -Y "tcp.flags.syn==1 || http.request" -T fields -e frame.number -e tcp.flags.str -e http.request.uri
strings http.pcap | grep hunter2
openssl req -x509 -newkey rsa:2048 -nodes -keyout k.pem -out c.pem -days 1 -subj /CN=localhost
openssl s_server -accept 8443 -cert c.pem -key k.pem -www -quiet &
sudo tcpdump -i lo -w tls.pcap -U port 8443 &   then   curl -sk https://127.0.0.1:8443/?user=alice&password=hunter2
tshark -r tls.pcap -Y tls.handshake -T fields -e frame.number -e tls.handshake.type
strings tls.pcap | grep -c hunter2
```

### What you should see

``` text
1  ··········S·                       <- SYN
2  ·······A··S·                       <- SYN-ACK
4  ·······AP···  /?user=alice&password=hunter2
hunter2 found in http.pcap: 1
4  1                                  <- TLS ClientHello
6  2                                  <- TLS ServerHello
hunter2 found in tls.pcap: 0
```

### Write in your lab notebook

- The three-way handshake frames and their flags.
- The plaintext request in the HTTP capture and its absence in the TLS capture.
- What TLS still leaks: IPs, ports, timing, sizes and (without ECH) the server name.

**Defence.** HTTPS everywhere with HSTS; never send secrets in URLs (they land in logs and history even over HTTPS).

## LAB 4. Hashing and cracking your own test hashes

About 30 minutes

**Why.** Explains in numbers why passwords need salt and a slow hash, and why long passphrases win.

**Setup.** python3 generated/security-labs/crack_lab.py (standard library only). It makes hashes of three test passwords and runs a 20-word dictionary attack on them.

### Steps

``` bash
python3 crack_lab.py
Edit TEST_PASSWORDS: add one of your old weak passwords' patterns (never a real current password) and run again
Change n=2**14 to 2**15 in scrypt() and compare the time
```

### What you should see

``` text
sunshine        MD5, no salt     CRACKED: sunshine   tried  7      0.04 ms
sunshine        scrypt + salt    CRACKED: sunshine   tried  7    355.11 ms
india123        SHA-256 + salt   CRACKED: india123   tried 18      0.03 ms
correct-horse-battery-staple  scrypt + salt  not found  tried 20  909.53 ms
```

### Write in your lab notebook

- Salt does not save a weak password from a dictionary attack; it stops precomputed tables and makes equal passwords hash differently.
- scrypt made each guess roughly ten thousand times slower than MD5 here: that is the whole point.
- The passphrase survived because it is not in any list, not because of the hash.

**Defence.** Store passwords with Argon2id, scrypt or bcrypt and a unique salt; check new passwords against breached lists; allow long passphrases (NIST SP 800-63B).

## LAB 5. Find and fix SQL injection and XSS

About 60 minutes

**Why.** The two web bugs every security interview and PortSwigger path starts with, found and fixed in code you control.

**Setup.** pip install flask; cd generated/security-labs; python app_vulnerable.py (serves on 127.0.0.1:5000). The fixed version is app_fixed.py on port 5001.

### Steps

``` sql
curl "http://127.0.0.1:5000/search?q=lap"                                  # normal
curl -G http://127.0.0.1:5000/search --data-urlencode "q=x' UNION SELECT name, password FROM users --"
curl -X POST -d "user=alice' --&password=anything" http://127.0.0.1:5000/login
curl -G http://127.0.0.1:5000/greet --data-urlencode "name=<script>alert(1)</script>"
Repeat all three against port 5001 (app_fixed.py)
Read the diff: parameterised queries, html.escape, Content-Security-Policy
python -m pytest -q test_labs.py
```

### What you should see

``` text
{"results": [["laptop", 60000]]}
{"results": [["alice", "wonderland"], ["bob", "builder"]]}       <- passwords leaked
welcome                                                    <- logged in with no password
<h1>Hello <script>alert(1)</script></h1>                  <- script runs
--- fixed app ---
{"results": []}   invalid   <h1>Hello &lt;script&gt;alert(1)&lt;/script&gt;</h1>
7 passed
```

### Write in your lab notebook

- Each payload, why it worked (the exact SQL or HTML it produced), and the one-line fix.
- Why escaping by hand is fragile and parameters are not.
- What the CSP header adds even if an escape is missed.

**Defence.** Parameterised queries everywhere, output encoding by context, a strict CSP, least-privilege database accounts.

## LAB 6. Detect a brute-force attack in a log

About 30 minutes

**Why.** The blue-team side: a SOC analyst writes rules like this, and it is a good small project to show.

**Setup.** Run app_vulnerable.py, then try 8 wrong passwords for bob (a loop of curl -X POST). Then run detect_bruteforce.py auth.log. Repeat against app_fixed.py.

### Steps

``` bash
for p in 123456 password qwerty letmein dragon monkey sunshine iloveyou; do curl -s -o /dev/null -w "%{http_code} " -X POST -d "user=bob&password=$p" http://127.0.0.1:5000/login; done
python detect_bruteforce.py auth.log
Same loop against port 5001
Change the rule: alert at 10 failures in 5 minutes; test it with the slow and fast examples in test_labs.py
```

### What you should see

``` text
401 401 401 401 401 401 401 401         <- vulnerable app never slows down
ALERT brute force from 127.0.0.1 at 2026-11-17 11:43:13 (last user tried: bob)
401 401 401 401 429 429 429 429         <- fixed app: lockout at the 5th failure from this IP
                                          (the alice' -- attempt in Lab 5 was the first)
```

### Write in your lab notebook

- The detection rule in one sentence and its false-positive risk (shared office IPs).
- Why lockout per IP is weak against password spraying from many IPs, and what helps (per-account limits, MFA).
- How you would send this alert to a SIEM.

**Defence.** Rate limits per IP and per account, MFA, alerting on failure bursts, and no difference in the error message for wrong user vs wrong password.
