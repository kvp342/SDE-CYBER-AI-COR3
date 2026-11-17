# Security

[All categories](README.md) · 10 topics

## Topics

- [OWASP Top 10](#owasp-top-10)
- [SQL injection](#sql-injection)
- [Cross-site scripting (XSS) and CSRF](#cross-site-scripting-xss-and-csrf)
- [Broken access control and IDOR](#broken-access-control-and-idor)
- [Server-side request forgery (SSRF)](#server-side-request-forgery-ssrf)
- [Hashing, encryption and passwords](#hashing-encryption-and-passwords)
- [Threat modelling (STRIDE)](#threat-modelling-stride)
- [Binary exploitation basics](#binary-exploitation-basics)
- [CTFs and security labs](#ctfs-and-security-labs)
- [Bug bounty and responsible disclosure](#bug-bounty-and-responsible-disclosure)

## OWASP Top 10

*Level 1: Core*

The shared language of AppSec. Even SDE interviewers are impressed when you name the risk in your own project.

**Key idea**

The OWASP Top 10 (2021) lists the most critical web risks: A01 Broken Access Control, A02 Cryptographic Failures, A03 Injection (incl. XSS), A04 Insecure Design, A05 Security Misconfiguration, A06 Vulnerable and Outdated Components, A07 Identification and Authentication Failures, A08 Software and Data Integrity Failures, A09 Security Logging and Monitoring Failures, A10 Server-Side Request Forgery.

Broken access control is #1: the app checks that you are logged in but not that you may access this object.


**Points**

- Authentication = who you are; authorisation = what you may do
- Defence in depth: validate input, encode output, least privilege, logging
- A09 is exactly what TenantWall's CloudTrail + CloudWatch alarm addresses

**Traps**

- Memorising the list without one exploit + one fix for each

**Interviewers ask**

- Name three OWASP risks and how you'd prevent them.
- Authentication vs authorisation?

**Practise**

- [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-labs)

**Learn more**

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org)

**Related:** [SQL injection](#sql-injection) · [Cross-site scripting (XSS) and CSRF](#cross-site-scripting-xss-and-csrf) · [Broken access control and IDOR](#broken-access-control-and-idor) · [Server-side request forgery (SSRF)](#server-side-request-forgery-ssrf)

[Back to the topic list](#topics)

## SQL injection

*Level 1: Core*

The classic vulnerability; first PortSwigger topic and a guaranteed security interview question.

**Key idea**

Happens when user input is concatenated into a SQL query, so the input changes the query's structure. ' OR '1'='1 turns a login check into 'always true'; UNION SELECT reads other tables; blind SQLi infers data from true/false or timing differences.

Fix: parameterised queries / prepared statements, which send the query and the data separately so data can never become code. Add least-privilege DB accounts and input validation as extra layers. Escaping by hand is fragile.


**Points**

- ORMs are safe unless you build raw queries with strings
- Second-order SQLi: stored input used later in a query

```text
// vulnerable
q = "SELECT * FROM users WHERE name = '" + name + "'";
// safe (prepared statement)
stmt = db.prepare("SELECT * FROM users WHERE name = ?"); stmt.bind(1, name);
```

**Traps**

- Thinking input filtering alone fixes it

**Interviewers ask**

- What is SQL injection and how do you prevent it?
- Why do prepared statements work?

**Practise**

- [PortSwigger: SQL injection labs](https://portswigger.net/web-security/sql-injection)

**Learn more**

- [PortSwigger: SQL injection](https://portswigger.net/web-security/sql-injection)
- [OWASP SQLi prevention cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

**Related:** [OWASP Top 10](#owasp-top-10) · [SQL for interviews](core-cs.md#sql-for-interviews)

[Back to the topic list](#topics)

## Cross-site scripting (XSS) and CSRF

*Level 1: Core*

The two most common client-side web bugs; asked in AppSec and full-stack interviews.

**Key idea**

XSS: attacker-controlled script runs in another user's browser on your site. Reflected (from the request), stored (saved in the database), DOM-based (client JS writes untrusted data into the page). Impact: steal session data, act as the user.

Fix XSS: context-aware output encoding (HTML, attribute, JS, URL), frameworks that escape by default, a Content-Security-Policy, HttpOnly cookies.

CSRF: a malicious site makes the victim's browser send an authenticated request (e.g. change email). Fix: SameSite cookies, anti-CSRF tokens, re-authentication for sensitive actions.


**Points**

- innerHTML with user data → DOM XSS
- SameSite=Lax is the modern default in browsers
- CORS is not a CSRF defence

**Traps**

- Confusing XSS (runs script) with CSRF (forges a request)

**Interviewers ask**

- Difference between XSS and CSRF?
- How does CSP help?

**Practise**

- [PortSwigger: XSS labs](https://portswigger.net/web-security/cross-site-scripting)
- [PortSwigger: CSRF labs](https://portswigger.net/web-security/csrf)

**Learn more**

- [PortSwigger: XSS](https://portswigger.net/web-security/cross-site-scripting)
- [PortSwigger: CSRF](https://portswigger.net/web-security/csrf)

**Related:** [OWASP Top 10](#owasp-top-10) · [HTTP, HTTPS and TLS](core-cs.md#http-https-and-tls)

[Back to the topic list](#topics)

## Broken access control and IDOR

*Level 2: Interview-ready*

OWASP #1 and the most common bug-bounty finding. Directly related to TenantWall's tenant isolation.

**Key idea**

IDOR (insecure direct object reference): the app uses an ID from the request (/invoice?id=1043) without checking the object belongs to the user. Change the ID, read someone else's data.

Other forms: missing function-level checks (normal user calls /admin API), privilege escalation via a role parameter, path traversal.

Fix: enforce authorisation on the server for every request and object (deny by default), centralise checks, use unguessable IDs only as extra defence, test with two accounts.


**Points**

- Multi-tenant SaaS: every query filtered by tenant\_id from the session, never from the request
- ABAC in TenantWall enforces this at the AWS layer with tags

**Traps**

- Relying on hidden UI elements as access control

**Interviewers ask**

- What is IDOR and how would you test for it?
- How do you enforce tenant isolation?

**Practise**

- [PortSwigger: access control labs](https://portswigger.net/web-security/access-control)

**Learn more**

- [PortSwigger: access control](https://portswigger.net/web-security/access-control)

**Related:** [OWASP Top 10](#owasp-top-10) · [ABAC: attribute-based access control](cloud.md#abac-attribute-based-access-control) · [AWS IAM and least privilege](cloud.md#aws-iam-and-least-privilege)

[Back to the topic list](#topics)

## Server-side request forgery (SSRF)

*Level 2: Interview-ready*

OWASP A10 and the bug behind major cloud breaches; ties web security to AWS.

**Key idea**

The server fetches a URL the attacker controls (image preview, webhook, PDF generator). The attacker points it at internal addresses: localhost admin panels, internal services, or the cloud metadata endpoint (169.254.169.254) to steal temporary IAM credentials.

Fix: allow-lists of destinations, block private and link-local ranges after DNS resolution, disable redirects, and on AWS require IMDSv2 (session tokens) and give instances least-privilege roles.


**Points**

- The 2019 Capital One breach involved SSRF + over-privileged IAM role
- flaws.cloud level 5 shows the metadata attack

**Traps**

- Blocking by string matching (bypassed with decimal IPs, DNS rebinding)

**Interviewers ask**

- What is SSRF and why is it dangerous in the cloud?

**Practise**

- [PortSwigger: SSRF labs](https://portswigger.net/web-security/ssrf)
- [flaws.cloud](http://flaws.cloud)

**Learn more**

- [PortSwigger: SSRF](https://portswigger.net/web-security/ssrf)

**Related:** [OWASP Top 10](#owasp-top-10) · [AWS IAM and least privilege](cloud.md#aws-iam-and-least-privilege) · [AWS core services and the SAA-C03 exam](cloud.md#aws-core-services-and-the-saa-c03-exam)

[Back to the topic list](#topics)

## Hashing, encryption and passwords

*Level 1: Core*

A common short question in security and backend interviews.

**Key idea**

Hashing is one-way and fixed-length (SHA-256): used for integrity and fingerprints. Encryption is reversible with a key: symmetric (AES, one shared key, fast) or asymmetric (RSA/ECC, public/private key pair, used for key exchange and signatures).

Passwords: never encrypt, never plain-hash. Use a slow, salted password hash (Argon2id, bcrypt, scrypt). The salt stops precomputed rainbow tables; slowness stops brute force.

Digital signatures: hash the message, sign with the private key; anyone verifies with the public key.


**Points**

- Encoding (Base64) is not encryption
- MAC/HMAC = integrity + authenticity with a shared key
- AES-GCM gives encryption + integrity

**Traps**

- Saying 'we hash with MD5' for passwords

**Interviewers ask**

- Hashing vs encryption?
- How should passwords be stored?
- Symmetric vs asymmetric?

**Learn more**

- [OWASP Password Storage cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [CryptoHack (free)](https://cryptohack.org)

**Related:** [HTTP, HTTPS and TLS](core-cs.md#http-https-and-tls) · [OWASP Top 10](#owasp-top-10)

[Back to the topic list](#topics)

## Threat modelling (STRIDE)

*Level 2: Interview-ready*

Lets you add 'I threat-modelled it' to any project answer. Security-engineer interviews ask you to do it live.

**Key idea**

Draw the system's data flow: users, processes, data stores, trust boundaries. For each element, ask STRIDE: Spoofing (identity), Tampering (data), Repudiation (no audit trail), Information disclosure, Denial of service, Elevation of privilege.

For each threat, record a mitigation and its priority. Four questions: what are we building, what can go wrong, what will we do about it, did we do a good job?


**Points**

- Trust boundaries are where most bugs live
- Repudiation → logging (CloudTrail)
- Elevation of privilege → IAM least privilege

**Traps**

- A list of threats with no mitigations

**Interviewers ask**

- Threat-model a login page.
- Threat-model your project.

**Learn more**

- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [Microsoft STRIDE](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)

**Related:** [OWASP Top 10](#owasp-top-10) · [TenantWall (your research project)](cloud.md#tenantwall-your-research-project)

[Back to the topic list](#topics)

## Binary exploitation basics

*Level 3: Advanced*

Your L3 security rung and the binary taster from the roadmap. It makes your C/C++ and OS memory knowledge concrete, which HFT and systems interviewers value.

**Key idea**

Stack layout: local buffers sit below the saved frame pointer and return address. Writing past a buffer (gets, strcpy without bounds) overwrites the return address and redirects execution.

Defences and bypasses: stack canaries (detect overwrite), NX/DEP (stack not executable → return-oriented programming chains existing code 'gadgets'), ASLR (randomised addresses → need an info leak), PIE, RELRO.

Other bug classes: format strings (printf(user)), use-after-free and double free on the heap, integer overflows. Tools: GDB with pwndbg, pwntools, Ghidra for reversing, checksec.


**Points**

- Start with pwn.college's program-security modules
- Write a short write-up for every challenge you solve
- Secure C++: bounds-checked containers, avoid raw C strings

**Traps**

- Jumping to heap exploitation before stack basics

**Interviewers ask**

- What is a buffer overflow and how do canaries and ASLR stop it?
- What is ROP?

**Practise**

- [pwn.college](https://pwn.college)
- [picoCTF](https://picoctf.org)
- [ROP Emporium](https://ropemporium.com)

**Learn more**

- [pwn.college](https://pwn.college)
- [Nightmare (free course)](https://guyinatuxedo.github.io)

**Related:** [Memory management and virtual memory](core-cs.md#memory-management-and-virtual-memory) · [Virtual functions and the vtable](core-cs.md#virtual-functions-and-the-vtable) · [CTFs and security labs](#ctfs-and-security-labs)

[Back to the topic list](#topics)

## CTFs and security labs

*Level 2: Interview-ready*

A proven hiring channel for security roles (see the KPMG story) and great resume proof.

**Key idea**

Jeopardy CTFs have categories: web, pwn (binary exploitation), reverse engineering, crypto, forensics, misc. Each solved challenge gives a flag.

Path: OverTheWire Bandit (Linux) → picoCTF (all categories, beginner) → PortSwigger labs (web) → pwn.college (binary) → live CTFs on CTFtime with a team.

Write up each solve on a blog or GitHub: problem, approach, the key insight, the fix. Write-ups are what recruiters can read.


**Points**

- Join or form a college team; India has many college CTFs
- Top-25% finish in a mid-rated CTF is a solid resume line

**Traps**

- Only reading write-ups without solving

**Interviewers ask**

- Tell me about a CTF challenge you solved.

**Practise**

- [OverTheWire Bandit](https://overthewire.org/wargames/bandit/)
- [picoCTF](https://picoctf.org)
- [CTFtime](https://ctftime.org)
- [TryHackMe](https://tryhackme.com)

**Learn more**

- [CTF101](https://ctf101.org)

**Related:** [Binary exploitation basics](#binary-exploitation-basics) · [Bug bounty and responsible disclosure](#bug-bounty-and-responsible-disclosure)

[Back to the topic list](#topics)

## Bug bounty and responsible disclosure

*Level 4: Elite*

An accepted report is proof no college name can match. It's your L4 security goal.

**Key idea**

Bug bounty programmes pay or credit researchers for reporting vulnerabilities within a defined scope. Read the scope and rules first; testing out of scope is illegal.

Start with recon on wide-scope programmes, focus on one bug class you know well (IDOR, access control, XSS), and read disclosed reports on HackerOne Hacktivity to learn what gets accepted.

Responsible disclosure: report privately, give details and impact, don't access more data than needed, wait for a fix before publishing.


**Points**

- Quality report: steps to reproduce, impact, fix suggestion
- Indian govt sites: report to CERT-In
- Duplicates are normal at first

**Traps**

- Running automated scanners against programmes that forbid them

**Interviewers ask**

- Walk me through a vulnerability you found.

**Practise**

- [HackerOne Hacktivity](https://hackerone.com/hacktivity)
- [Bugcrowd](https://bugcrowd.com)

**Learn more**

- [PortSwigger Academy](https://portswigger.net/web-security)
- [HackerOne Hacker101 (free)](https://www.hacker101.com)

**Related:** [Broken access control and IDOR](#broken-access-control-and-idor) · [CTFs and security labs](#ctfs-and-security-labs)

[Back to the topic list](#topics)
