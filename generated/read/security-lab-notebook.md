SECURITY · LAB NOTEBOOK

# Security lab notebook

Templates for writing up CTF challenges and PortSwigger labs (with a worked example of each), a STRIDE threat model of TenantWall, a command sheet for labs, and a web-security sheet by vulnerability class. Good write-ups are the evidence behind "security" on your resume: publish them on GitHub or a blog.

**Rules.** Practise only on platforms built for it (OverTheWire, PortSwigger Web Security Academy, picoCTF, TryHackMe, your own VMs) or systems you have written permission to test. Do not publish flags or passwords that a platform asks you to keep private.

|                                                      |
|------------------------------------------------------|
| [CTF write-up template and example](#ctf-write-up)         |
| [PortSwigger lab note template and example](#portswigger-lab-note) |
| [STRIDE threat model of TenantWall](#stride-threat-model-tenantwall)         |
| [Linux and networking commands](#linux-and-networking-commands)             |
| [Web security by vulnerability class](#web-security-by-vulnerability-class)      |

## CTF write-up

### Template

1.  Challenge: name, platform, category, difficulty, date
2.  Goal: what the flag or win condition is
3.  Recon: what you looked at first and what you noticed
4.  Dead ends: what you tried that failed, and why (interviewers like this part)
5.  Solution: the steps that worked, with the commands you ran
6.  Root cause: the weakness in one sentence
7.  Fix: how a developer or admin would prevent it
8.  Learned: one technique to reuse, and a Knowledge Base page to revisit

### Worked example

|            |                                                                                                                                                                   |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Challenge  | OverTheWire Bandit, level 0 → 1 (Linux basics), beginner                                                                                                          |
| Goal       | Log in over SSH and find the password for the next level.                                                                                                         |
| Recon      | The level page gives the host bandit.labs.overthewire.org, port 2220, user bandit0. After logging in, ls shows a file named readme in the home directory.         |
| Dead ends  | ssh without -p tried port 22 and was refused: the port matters.                                                                                                   |
| Solution   | ssh -p 2220 bandit0@bandit.labs.overthewire.org, then cat readme. The file holds the next password (not written here: the site asks players not to publish them). |
| Root cause | None: this level teaches SSH and reading files.                                                                                                                   |
| Fix        | Not applicable; later levels add permissions, hidden files and SUID binaries.                                                                                     |
| Learned    | Always read the level page for the port and hints; ls -la shows hidden files.                                                                                     |

Level page: [overthewire.org/wargames/bandit](https://overthewire.org/wargames/bandit/). Knowledge Base: [CTF](knowledge-base/security.md#ctfs-and-security-labs).

## PortSwigger lab note

### Template

1.  Lab: title and link, topic, level (Apprentice / Practitioner / Expert)
2.  Vulnerable feature: which request or parameter
3.  Hypothesis: what you expected and why
4.  Proof: the request you changed and the response that confirmed it
5.  Impact: what an attacker gains
6.  Fix: the code-level fix, plus a defence-in-depth layer
7.  Time taken and whether you needed the solution

### Worked example

|                    |                                                                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| Lab                | SQL injection vulnerability in WHERE clause allowing retrieval of hidden data (Apprentice)                                        |
| Vulnerable feature | The product category filter: /filter?category=Gifts                                                                               |
| Hypothesis         | The category is concatenated into SELECT … WHERE category = '…' AND released = 1.                                                 |
| Proof              | A category value of ' OR 1=1-- made the condition always true and commented out the released check; unreleased products appeared. |
| Impact             | Reading data the application meant to hide; similar flaws can expose whole tables.                                                |
| Fix                | Parameterised query; least-privilege database account; generic error pages.                                                       |
| Time               | 15 minutes, no solution needed.                                                                                                   |

All labs: [portswigger.net/web-security/all-labs](https://portswigger.net/web-security/all-labs). Knowledge Base: [SQL injection](knowledge-base/security.md#sql-injection).

## STRIDE threat model: TenantWall

Asset: each tenant's objects and instances. Attacker: a tenant, or anyone with a stolen tenant credential. Trust boundary: the IAM policy evaluation between tenant roles and shared resources.

| Threat                 | Example in TenantWall                                                                       | Mitigation                                                                                                                              |
|------------------------|---------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| Spoofing               | Stolen tenant credentials or long-lived access keys used by someone else                    | Roles with temporary credentials; MFA on human users; short session duration; no access keys in code                                    |
| Tampering              | A tenant re-tags a resource or itself to another tenant; someone edits or deletes log files | Explicit deny on tag changes (aws:TagKeys); CloudTrail log file validation; S3 Object Lock or a separate log account                    |
| Repudiation            | A tenant denies having accessed or changed data                                             | CloudTrail management and S3 data events; logs in a bucket tenants cannot write to                                                      |
| Information disclosure | Tenant A reads tenant B's objects; a bucket becomes public; data read over plain HTTP       | ABAC prefix and tag conditions plus explicit deny; S3 Block Public Access; bucket policy denying aws:SecureTransport = false; SSE-KMS   |
| Denial of service      | A tenant deletes or overwrites another's data, or runs up costs (data events, requests)     | Isolation as above; S3 versioning; AWS Budgets alerts; CloudWatch alarms on unusual request counts                                      |
| Elevation of privilege | A tenant attaches policies to itself or passes a more powerful role                         | No iam:Attach\*/Put\*/PassRole for tenant roles; permission boundaries; Access Analyzer checks; the AccessDenied alarm catches attempts |

Use this table in the paper's threat-model section; the mitigations map to the policies in `generated/tenantwall/`. Knowledge Base: [threat modelling](knowledge-base/security.md#threat-modelling-stride), [TenantWall](knowledge-base/cloud.md#tenantwall-your-research-project).

## Linux and networking commands

### Files

|                                          |                                                         |
|------------------------------------------|---------------------------------------------------------|
| `ls -la`                                 | list all files, including hidden ones, with permissions |
| `find / -perm -4000 -type f 2>/dev/null` | SUID binaries (privilege escalation check)              |
| `grep -rni 'password' .`                 | search recursively, case-insensitive, with line numbers |
| `chmod 600 key.pem`                      | owner read/write only                                   |
| `file x; strings x | less`               | what a file is; readable text inside a binary           |
| `sha256sum x`                            | hash to check integrity                                 |

### Processes and users

|                                   |                                       |
|-----------------------------------|---------------------------------------|
| `ps aux`                          | every process with its owner          |
| `sudo -l`                         | what you may run with sudo            |
| `id; whoami`                      | your user and groups                  |
| `journalctl -u ssh --since today` | service logs (systemd)                |
| `tail -f /var/log/auth.log`       | follow login attempts (Debian/Ubuntu) |

### Network

|                                |                                                        |
|--------------------------------|--------------------------------------------------------|
| `ip a`                         | interfaces and addresses                               |
| `ss -tulpn`                    | listening ports and the process behind each            |
| `ping -c 4 host`               | reachability                                           |
| `traceroute host`              | path to a host                                         |
| `dig example.com A +short`     | DNS lookup                                             |
| `curl -sI https://example.com` | response headers only                                  |
| `nc -zv host 1-1024`           | simple port check (only on systems you may test)       |
| `nmap -sV -p- target`          | service scan (only on systems you are allowed to scan) |
| `tcpdump -i any port 53`       | capture DNS packets (needs root)                       |

### Encoding and transfer

|                                |                                  |
|--------------------------------|----------------------------------|
| `echo aGk= | base64 -d`        | decode base64                    |
| `xxd file | head`              | hex dump                         |
| `ssh -p 2220 user@host`        | SSH to a non-default port        |
| `scp -P 2220 user@host:file .` | copy a file over SSH (capital P) |

Scanning tools (nmap, nc, tcpdump) only on machines you own or are allowed to test.

## Web security by vulnerability class

| Class                                                                             | Cause                                                                 | How to spot it                                              | Fix                                                                  |
|-----------------------------------------------------------------------------------|-----------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------|
| [SQL injection](https://portswigger.net/web-security/sql-injection)               | Input concatenated into a SQL query                                   | Quote or boolean changes alter results or errors            | Parameterised queries; least-privilege DB user                       |
| [Cross-site scripting](https://portswigger.net/web-security/cross-site-scripting) | Unescaped input rendered as HTML or JavaScript                        | Input reflected in the page or DOM unencoded                | Context-aware output encoding; CSP; HttpOnly cookies                 |
| [CSRF](https://portswigger.net/web-security/csrf)                                 | A site performs actions using cookies the browser sends automatically | State-changing requests without a token or SameSite cookies | CSRF tokens; SameSite=Lax/Strict; re-auth for sensitive actions      |
| [Access control / IDOR](https://portswigger.net/web-security/access-control)      | The app checks login but not ownership                                | Change an id in a URL or body and see another user's data   | Check ownership on every request server-side; deny by default        |
| [Authentication](https://portswigger.net/web-security/authentication)             | Weak login, reset or session handling                                 | No rate limit, user enumeration, predictable reset tokens   | Rate limits, MFA, generic errors, strong session handling            |
| [SSRF](https://portswigger.net/web-security/ssrf)                                 | The server fetches a URL the user controls                            | A URL parameter that the server requests                    | Allowlist destinations; block internal ranges and metadata endpoints |
| [Path traversal](https://portswigger.net/web-security/file-path-traversal)        | File names from input reach the file system                           | ../ sequences change which file is read                     | Map ids to files; canonicalise and check the base directory          |
| [OS command injection](https://portswigger.net/web-security/os-command-injection) | Input reaches a shell command                                         | Separators such as ; or \| change behaviour                 | Avoid the shell; pass arguments as a list; validate strictly         |
| [XXE](https://portswigger.net/web-security/xxe)                                   | XML parser resolves external entities                                 | XML input accepted with a DOCTYPE                           | Disable DTDs and external entities in the parser                     |
| [Insecure deserialization](https://portswigger.net/web-security/deserialization)  | Untrusted data turned into objects                                    | Serialised objects in cookies or parameters                 | Do not deserialise untrusted data; use JSON with schemas; sign data  |
| [File upload](https://portswigger.net/web-security/file-upload)                   | Uploaded files executed or served unsafely                            | Upload accepts any type or keeps the name                   | Allowlist types, rename, store outside the web root, scan            |
| [CORS misconfiguration](https://portswigger.net/web-security/cors)                | Any origin allowed to read responses with credentials                 | Access-Control-Allow-Origin reflects the request origin     | Fixed allowlist; never \* with credentials                           |
| [JWT flaws](https://portswigger.net/web-security/jwt)                             | Token signature not verified properly                                 | alg changes accepted, weak secrets, no expiry check         | Fix the algorithm list, strong secret or keys, check exp             |

Each class links to its PortSwigger Web Security Academy topic, which has free labs. Knowledge Base: [OWASP Top 10](knowledge-base/security.md#owasp-top-10).
