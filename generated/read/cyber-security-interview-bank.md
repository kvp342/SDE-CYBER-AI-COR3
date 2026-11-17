SECURITY ROLES · INTERVIEW BANK

# 97 security questions with model answers

For security-aware SDE, SOC, cloud-security and application-security interviews. It goes past the Knowledge Base's security pages: networks, web, cryptography, identity and cloud, incident response, Linux and Windows, and scenario questions. Facts that can be computed (ports, hash sizes, subnet maths, permission bits) were checked by script; the rest follow the official documents listed under each section.

| Section                                            |
|----------------------------------------------------|
| [1. Fundamentals](#01-fundamentals)                         |
| [2. Network security](#02-network-security)                     |
| [3. Web application security](#03-web-application-security)             |
| [4. Cryptography](#04-cryptography)                         |
| [5. Identity, access and cloud](#05-identity-access-and-cloud)           |
| [6. Incident response, SOC and forensics](#06-incident-response-soc-and-forensics) |
| [7. Linux, Windows and Active Directory](#07-linux-windows-and-active-directory)  |
| [8. Scenario questions](#08-scenario-questions)                   |

**How to use.** Cover the answer, say yours aloud in under a minute, then compare. Mark the ones you missed and redo them in 1, 3, 7 and 21 days. Before a security interview, read the scenario section twice: interviewers judge the order of your steps as much as the facts.

## 01. Fundamentals

Asked in every security round, often as the first question. Answer in one line, then give an example.

Q1What is the CIA triad?

Confidentiality (only the right people can read), Integrity (data is not changed without detection), Availability (it works when needed). Example: encryption protects C, hashes and signatures protect I, redundancy and rate limits protect A.

Q2Threat, vulnerability, risk: what is the difference?

A vulnerability is a weakness; a threat is something that could exploit it; risk is likelihood × impact of that happening. An unpatched server is a vulnerability; a botnet scanning for it is a threat; the risk depends on what the server holds.

Q3What is defence in depth?

Several independent layers, so one failure is not a breach: for a web app, a WAF, input validation, parameterised queries, least-privilege database users, encryption at rest and monitoring.

Q4What is the principle of least privilege?

Give each user, process and service only the permissions it needs, for only as long as it needs them. It limits the blast radius of a stolen credential or a bug.

Q5What is zero trust?

Never trust a request because of where it comes from (inside the network). Every request is authenticated, authorised and checked for device and context, and access is granted per resource.

Q6CVE, CWE and CVSS: what are they?

CVE is an ID for one specific known vulnerability; CWE is a category of weakness (for example CWE-89, SQL injection); CVSS is a 0–10 severity score for a vulnerability.

Q7Vulnerability scan vs penetration test?

A scan is automated and lists possible known issues; a pentest is a human-led, scoped and authorised attempt to exploit them and show real impact, with fewer false positives.

Q8Red team, blue team, purple team?

Red attacks (emulates adversaries), blue defends (detects and responds), purple is both working together so every red finding becomes a blue detection.

Q9Why is 'security through obscurity' weak on its own?

Hiding how something works delays an attacker but does not stop one who finds out. It is fine as an extra layer, never as the only one (Kerckhoffs: a system must be secure even if everything except the key is public).

Q10What is a zero-day?

A vulnerability that is exploited before the vendor has released a fix, so defenders have had zero days to patch.

Q11What is the attack surface and how do you reduce it?

Everything an attacker can reach: open ports, endpoints, inputs, accounts, dependencies. Reduce it by removing unused services and features, closing ports, and limiting who can reach admin interfaces.

Q12What is non-repudiation?

Proof that a party did something, so they cannot deny it later, usually through digital signatures plus trustworthy logs.

**Read more:** [NIST glossary (CSRC)](https://csrc.nist.gov/glossary) · [MITRE CWE](https://cwe.mitre.org/) · [FIRST CVSS](https://www.first.org/cvss/)

## 02. Network security

Expect follow-ups that go one layer deeper each time. Draw the packets if you can.

Q13Walk through the TCP three-way handshake.

Client sends SYN with its initial sequence number; server replies SYN-ACK with its own number and acknowledges the client's; client sends ACK. Both sides now know the other can send and receive.

Q14What is a SYN flood and how is it mitigated?

The attacker sends many SYNs without completing the handshake, filling the server's half-open connection table. Mitigations: SYN cookies (no state until the ACK arrives), rate limiting, and upstream DDoS scrubbing.

Q15Stateful vs stateless firewall?

A stateless filter checks each packet against rules on its own; a stateful firewall tracks connections, so return traffic for an allowed connection is permitted automatically. AWS NACLs are stateless; security groups are stateful.

Q16IDS vs IPS?

An IDS watches and alerts; an IPS sits inline and can block. An IPS false positive drops real traffic, so it is tuned more carefully.

Q17Signature-based vs anomaly-based detection?

Signatures match known bad patterns (few false positives, misses new attacks); anomaly detection flags deviations from a baseline (can catch new attacks, more false positives).

Q18What is ARP spoofing?

On a LAN, the attacker sends forged ARP replies so victims map the gateway's IP to the attacker's MAC, putting the attacker in the middle. Defences: dynamic ARP inspection, static entries for critical hosts, encryption (TLS) so interception reveals nothing useful.

Q19What is DNS cache poisoning and what stops it?

Forged DNS responses get cached by a resolver, sending users to the attacker's IP. Defences: source-port and query-ID randomisation, DNSSEC signatures, and TLS so a wrong server cannot present a valid certificate.

Q20Default ports: SSH, DNS, HTTP, HTTPS, RDP, SMB, MySQL?

SSH 22, DNS 53, HTTP 80, HTTPS 443, RDP 3389, SMB 445, MySQL 3306.

Q21Nmap: SYN scan vs connect scan?

-sS sends SYN and resets on SYN-ACK (never completes the handshake, needs raw-socket privileges); -sT uses the OS connect() call and completes it (no privileges needed, more likely to be logged).

Q22What does a /26 give you?

64 addresses (2^6), of which 62 are usable hosts in a traditional subnet (network and broadcast reserved). AWS reserves 5 per subnet, leaving 59.

Q23IPsec VPN vs TLS VPN?

IPsec works at the network layer and tunnels all IP traffic (site-to-site is common); TLS VPNs work above TCP/UDP, pass through most firewalls on 443, and suit remote users.

Q24How would you mitigate a volumetric DDoS?

You cannot absorb it at the server: use an upstream scrubbing service or CDN (anycast spreads load), rate limits, autoscaling for the application layer, and a runbook to contact the provider.

Q25What is network segmentation and why does it matter?

Splitting a network into zones (VLANs, subnets, security groups) with controlled traffic between them, so one compromised host cannot reach everything (limits lateral movement).

**Read more:** [RFC 9293: TCP](https://www.rfc-editor.org/rfc/rfc9293) · [Nmap reference guide](https://nmap.org/book/man.html) · [IANA port registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)

## 03. Web application security

The kit's OWASP map covers the basics; these are the follow-ups interviewers move to next.

Q26Stored, reflected and DOM-based XSS?

Stored: the payload is saved on the server and served to every viewer. Reflected: it comes back in the response to a crafted link. DOM-based: client-side JavaScript writes untrusted data into the page without the server being involved.

Q27What does a Content Security Policy do?

A response header that tells the browser which sources of scripts, styles and other content are allowed. A strict CSP (no inline scripts, nonces or hashes) stops most injected scripts from running even if XSS exists.

Q28What does the SameSite cookie attribute do?

Controls whether the cookie is sent on cross-site requests. Lax (Chrome's default when the attribute is missing) sends it only on top-level cross-site GET navigations; Strict never on cross-site; None always (requires Secure). It is a strong CSRF defence.

Q29What do HttpOnly and Secure mean on a cookie?

HttpOnly: JavaScript cannot read it (limits session theft through XSS). Secure: only sent over HTTPS.

Q30Explain CORS. Is it a security control?

CORS lets a server relax the browser's same-origin policy for chosen origins. It protects users' browsers, not your server: a misconfigured CORS (reflecting any origin with credentials) lets other sites read authenticated responses.

Q31What is IDOR and how do you prevent it?

Insecure direct object reference: changing an ID in a request (/orders/1002) returns someone else's data because the server checks only that you are logged in. Prevent it with an ownership or policy check on every object access.

Q32What is path traversal?

User input such as ../../etc/passwd escapes the intended directory. Prevent it by resolving the full path and checking it stays under the base directory, or by mapping IDs to files instead of using names.

Q33What is XXE?

XML external entity injection: a parser that resolves external entities can be made to read local files or make server-side requests. Disable DTDs and external entities in the parser.

Q34What is clickjacking and the fix?

A hostile page loads your site in an invisible frame and tricks clicks. Fix: Content-Security-Policy frame-ancestors (or X-Frame-Options: DENY).

Q35What is session fixation?

The attacker makes the victim use a session ID the attacker knows, then waits for them to log in. Fix: issue a new session ID at login and privilege changes.

Q36Common JWT mistakes?

Accepting alg=none or switching algorithms, weak HMAC secrets, not checking expiry or audience, storing sensitive data in the (only encoded, not encrypted) payload, and having no way to revoke tokens.

Q37How do you prevent SQL injection beyond 'use prepared statements'?

Parameterised queries everywhere (including ORDER BY via allow-lists), least-privilege database accounts, input validation, no detailed database errors to users, and a WAF as an extra layer.

Q38What is a deserialisation vulnerability?

Deserialising untrusted data with a format that can construct arbitrary objects (Java serialization, Python pickle) can run attacker-chosen code. Use data-only formats such as JSON with a schema.

Q39What is rate limiting protecting against on a login API?

Brute force and credential stuffing. Combine per-account and per-IP limits, backoff, MFA, and breached-password checks; do not reveal whether the username exists.

**Read more:** [MDN: Web security](https://developer.mozilla.org/en-US/docs/Web/Security) · [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) · [PortSwigger Web Security Academy](https://portswigger.net/web-security)

## 04. Cryptography

You are not expected to do maths. You are expected to choose the right tool and explain why.

Q40Symmetric vs asymmetric encryption?

Symmetric uses one shared key (AES): fast, but the key must be shared securely. Asymmetric uses a public/private key pair (RSA, elliptic curves): slower, solves key exchange and enables signatures. TLS uses asymmetric to agree a key, then symmetric for data.

Q41Encoding vs encryption vs hashing?

Encoding (Base64) changes the format and is reversible by anyone; encryption is reversible only with the key; hashing is one-way and fixed-length.

Q42Output sizes of MD5, SHA-1 and SHA-256?

128, 160 and 256 bits (32, 40 and 64 hex characters). MD5 and SHA-1 are broken for collision resistance; use SHA-256 or better.

Q43Why salt passwords, and why bcrypt or Argon2 instead of SHA-256?

A unique random salt per password makes precomputed tables useless and identical passwords hash differently. bcrypt, scrypt and Argon2 are deliberately slow and tunable, so guessing is expensive; SHA-256 is designed to be fast.

Q44What is HMAC?

A keyed hash: HMAC(key, message) proves the message came from someone with the key and was not changed. Used for API request signing and JWT HS256.

Q45Why is AES-ECB mode bad?

Identical plaintext blocks give identical ciphertext blocks, so patterns leak (the famous encrypted penguin image). Use an authenticated mode such as AES-GCM.

Q46What does AES-GCM give you that AES-CBC does not?

Authentication: GCM detects tampering. CBC alone gives only confidentiality and has been attacked through padding oracles. GCM needs a unique nonce per key for every message.

Q47What is a digital signature?

The sender signs a hash of the message with their private key; anyone verifies with the public key. Gives integrity, authenticity and non-repudiation, not confidentiality.

Q48How does a browser trust a certificate?

The server's certificate is signed by an intermediate CA, which is signed by a root CA in the browser's trust store. The browser checks the chain, the hostname, the validity dates and revocation.

Q49What is Diffie-Hellman for?

Two parties agree a shared secret over a public channel without sending it. Ephemeral DH (ECDHE) is the key exchange used in TLS 1.3.

Q50What is perfect forward secrecy?

Session keys come from ephemeral key exchanges, so stealing the server's long-term private key later does not decrypt past recorded traffic. TLS 1.3 requires it.

Q51TLS 1.3 vs TLS 1.2 in one line?

TLS 1.3 removed weak options (RSA key transport, static DH, CBC suites), always gives forward secrecy, and completes the handshake in one round trip.

Q52What do current NIST guidelines say about password rules?

Favour length over composition rules, check new passwords against breached and common lists, do not force periodic changes without evidence of compromise, and allow paste and password managers.

**Read more:** [NIST SP 800-63B (passwords)](https://pages.nist.gov/800-63-4/sp800-63b.html) · [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446) · [RFC 2104: HMAC](https://www.rfc-editor.org/rfc/rfc2104)

## 05. Identity, access and cloud

Your TenantWall work lives here. Tie answers back to it when you can.

Q53OAuth 2.0 vs OpenID Connect?

OAuth 2.0 is for delegated authorisation (an app gets an access token to call an API on your behalf). OpenID Connect adds authentication on top: an ID token that says who the user is.

Q54Why use the authorization code flow with PKCE for apps?

The code is exchanged for tokens server-to-server, and PKCE binds the exchange to the client that started it, so an intercepted code is useless. The implicit flow returned tokens in the URL and is no longer recommended.

Q55RBAC vs ABAC?

RBAC grants permissions through roles (simple, but roles multiply). ABAC decides from attributes of the user, resource and context (for example tenant tag equals the principal's tag), so one policy covers many tenants.

Q56What is the shared responsibility model?

The cloud provider secures the cloud (hardware, facilities, hypervisor); the customer secures what they put in it (IAM, data, network rules, OS patches on EC2). Misconfiguration is the customer's side.

Q57How does AWS evaluate a request across policies?

Default deny; an explicit deny anywhere wins; otherwise it needs an allow from an applicable policy, and limits such as SCPs, permission boundaries and session policies must also allow it.

Q58Security groups vs NACLs?

Security groups: stateful, attached to instances or interfaces, allow rules only. NACLs: stateless, at the subnet level, allow and deny rules evaluated in number order.

Q59Why IMDSv2?

It requires a session token obtained with a PUT request and a hop limit, which blocks most SSRF attacks that try to read instance credentials from the metadata service.

Q60What is envelope encryption (KMS)?

Data is encrypted with a data key; the data key is encrypted with a key held in KMS. Only the small data key goes to KMS, and access is controlled and logged through KMS key policies.

Q61How do you stop S3 data leaks?

Account-level Block Public Access, bucket policies with least privilege, default encryption, no wildcard principals, access logging or CloudTrail data events, and regular checks with IAM Access Analyzer.

Q62Long-lived access keys vs roles?

Roles give temporary credentials that expire and rotate automatically; long-lived keys leak through code and logs. Use roles for services and SSO for people; rotate and alert on any remaining keys.

Q63What is MFA, and which factors resist phishing?

Two or more of something you know, have and are. Codes by SMS or app can be phished in real time; FIDO2/WebAuthn security keys and passkeys resist phishing because they are bound to the website's origin.

Q64What is privilege escalation in IAM terms?

A principal with a permission such as iam:PassRole, iam:CreatePolicyVersion or iam:AttachUserPolicy can grant itself more access. Review these permissions especially carefully.

**Read more:** [AWS IAM policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) · [AWS shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/) · [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html) · [AWS: IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)

## 06. Incident response, SOC and forensics

For SOC and blue-team roles. Show that you contain first, preserve evidence, and communicate.

Q65What are the phases of incident response?

The classic NIST SP 800-61 Rev. 2 cycle: Preparation; Detection and Analysis; Containment, Eradication and Recovery; Post-Incident Activity. Rev. 3 (2025) maps the same work onto the NIST CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond, Recover).

Q66What is the order of volatility?

Collect the most short-lived evidence first: CPU registers and cache, then routing and ARP tables, process table and memory, then temporary files, then disk, then remote logs, then archives (RFC 3227).

Q67What is chain of custody?

A record of who collected each piece of evidence, when, how, and every hand-over since, with hashes to show it was not changed. Without it, evidence may be unusable.

Q68IOC vs IOA?

An indicator of compromise is evidence that an attack happened (a malicious hash, IP or domain). An indicator of attack is behaviour that shows an attack in progress (for example a credential dump followed by lateral movement), useful before known IOCs exist.

Q69What does a SIEM do?

Collects logs from many sources, normalises them, correlates events with rules, raises alerts and keeps data for investigation and compliance (examples: Splunk, Microsoft Sentinel, Elastic).

Q70What does EDR add over antivirus?

Continuous recording of endpoint behaviour (processes, network connections, file changes), detection of suspicious behaviour, and response actions such as isolating the host, not just signature scanning.

Q71What is MITRE ATT&CK?

A public knowledge base of adversary tactics (the goal, for example Credential Access) and techniques (how, for example OS Credential Dumping, T1003), used to map detections and find gaps.

Q72How do you triage a reported phishing email?

Get the original with headers; check sender, SPF/DKIM/DMARC results and links or attachments in a sandbox; search the mail system for other recipients; remove the messages; block indicators; check if anyone clicked or entered credentials, and reset those.

Q73First steps when ransomware is detected?

Isolate affected hosts from the network (do not power them off, so memory is kept), disable compromised accounts, protect backups, identify the strain and scope, notify the incident lead and legal, then restore from clean backups.

Q74What makes a good alert?

High signal (few false positives), clear context (who, what, where), a severity, and a linked runbook. Tune or remove alerts that analysts always close.

Q75Which Windows event IDs mean a successful logon, a failed logon and a new account?

4624 successful logon, 4625 failed logon, 4720 user account created (also 4672: special privileges assigned to a new logon).

Q76What logs would you want from a web app during an incident?

Access logs with timestamps, source IPs and user IDs; authentication events; admin actions; errors; WAF and load-balancer logs; cloud audit logs (CloudTrail), all time-synchronised and centrally stored.

**Read more:** [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) · [RFC 3227: evidence collection](https://www.rfc-editor.org/rfc/rfc3227) · [MITRE ATT&CK](https://attack.mitre.org/)

## 07. Linux, Windows and Active Directory

Quick facts first, then the attack and the defence.

Q77What does chmod 750 mean?

Owner rwx (7), group r-x (5), others nothing (0).

Q78What is the SUID bit and why is it risky?

An SUID executable runs with its owner's privileges (often root). A writable or exploitable SUID binary is a classic privilege-escalation path. Find them with find / -perm -4000.

Q79Where are Linux password hashes stored?

In /etc/shadow, readable only by root. /etc/passwd holds account details and an 'x' placeholder.

Q80Common Linux persistence spots to check?

Cron jobs, systemd services and timers, ~/.ssh/authorized_keys, shell start-up files (.bashrc), and new users or sudoers entries.

Q81How do you see what is listening on a Linux host?

ss -tulpn (TCP and UDP listening sockets with the owning process); then check each unexpected one with ps and the binary path.

Q82What is sudo misconfiguration?

Rules such as NOPASSWD on an editor, a pager or find let a user spawn a root shell from inside that program (GTFOBins lists them). Grant only the exact commands needed.

Q83How does Kerberos authentication work at a high level?

The user gets a Ticket-Granting Ticket from the KDC after proving their password; they then request service tickets with the TGT; services accept the ticket without seeing the password.

Q84What is pass-the-hash?

With NTLM, the password hash itself works as the credential, so an attacker who dumps it from memory can authenticate without knowing the password. Defences: Credential Guard, LAPS, limiting admin logons, and preferring Kerberos.

Q85What is Kerberoasting?

Any domain user can request service tickets for accounts with SPNs; part of each ticket is encrypted with the service account's password hash, so it can be cracked offline. Defence: long random service-account passwords or managed service accounts.

Q86NTLM vs Kerberos?

NTLM is a challenge-response protocol without mutual authentication and is open to relay and pass-the-hash; Kerberos uses tickets from a trusted KDC, supports mutual authentication and is the default in Active Directory.

Q87What is lateral movement?

Using a foothold to reach other systems, for example with stolen credentials over RDP, SMB or WinRM. Segmentation, unique local admin passwords and logon monitoring limit it.

**Read more:** [Linux man pages: chmod](https://man7.org/linux/man-pages/man1/chmod.1.html) · [Microsoft Learn: Kerberos authentication](https://learn.microsoft.com/en-us/windows-server/security/kerberos/kerberos-authentication-overview) · [GTFOBins](https://gtfobins.github.io/)

## 08. Scenario questions

Structure every answer: clarify scope, contain, investigate, fix the root cause, prevent it happening again, and communicate.

Q88An AWS access key was pushed to a public GitHub repo. What now?

Deactivate the key immediately, then delete it; check CloudTrail for every action taken with it since the push; look for new users, keys, roles, instances and changed policies; remove the secret from git history; add secret scanning and pre-commit hooks; move the workload to roles.

Q89Your web server's CPU is at 100% and there is outbound traffic to an unknown IP. Walk through it.

Snapshot or isolate (security group) rather than shut down; capture memory and process list; find the process and its parent, binary and start-up entry; check how it got in (web logs, recent changes); rebuild from a clean image, patch, rotate credentials, and add detection for the indicator.

Q90A user says they entered their password on a fake login page. What do you do?

Reset the password and revoke sessions and tokens; check sign-in logs for logins from new places; check mailbox rules and MFA devices for changes; block the phishing domain; find other recipients; brief the user, no blame.

Q91You find an IDOR in production during a code review. What happens next?

Report it to the owner and security lead privately; assess exposure (logs of access to other users' IDs); ship the fix with an ownership check and a test; decide on user notification with legal; add the check as a shared middleware so it cannot be missed again.

Q92Design a secure password reset flow.

Same response whether or not the email exists; a single-use, random, short-lived token stored hashed; link sent to the registered email only; invalidate other sessions after reset; rate-limit requests; notify the user that the password changed.

Q93How would you secure a new microservice before launch?

Threat model it (STRIDE), authenticate every call (mTLS or signed tokens), authorise per resource, validate input, keep secrets in a manager, use least-privilege roles, log security events, scan dependencies and images in CI, and run a review or pentest.

Q94A developer wants to disable TLS certificate checks because of an error. What do you say?

No: it removes protection against interception. Find the cause instead (missing intermediate certificate, wrong hostname, expired certificate, or a corporate proxy CA that needs adding to the trust store).

Q95An alert shows 500 failed logins for one account from 50 IPs in an hour. Next steps?

Likely password spraying or brute force. Check for any success from those IPs, temporarily protect the account (lock or step-up MFA), block or rate-limit the sources, check other accounts for the same pattern, and confirm with the user.

Q96How would you explain a critical vulnerability to a non-technical manager?

What could happen in business terms, how likely it is, what we are doing and by when, and what we need from them. One paragraph, no jargon, with a clear decision if one is needed.

Q97You are asked to scan a partner's network 'quickly'. What do you need first?

Written authorisation from someone who owns those systems, an agreed scope (IP ranges, times, techniques), and contacts in case something breaks. Scanning without permission can be illegal.

**Read more:** [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) · [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/welcome.html)
