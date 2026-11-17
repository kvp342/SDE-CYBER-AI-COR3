"""Lab 4: make your OWN test hashes, then try a small dictionary attack on them. Never use real people's hashes.
Shows why unsalted fast hashes fall instantly, why salt stops precomputed tables, and why a slow hash (scrypt) costs attackers time."""
import hashlib, os, time
WORDLIST = ["123456", "password", "qwerty", "letmein", "dragon", "monkey", "sunshine", "iloveyou", "admin", "welcome",
            "football", "princess", "shadow", "superman", "trustno1", "hello123", "summer2024", "india123", "cricket", "pass@123"]
TEST_PASSWORDS = ["sunshine", "india123", "correct-horse-battery-staple"]       # the last one is not in the list
def md5(p): return hashlib.md5(p.encode()).hexdigest()
def sha256_salted(p, salt): return hashlib.sha256(salt + p.encode()).hexdigest()
def scrypt(p, salt): return hashlib.scrypt(p.encode(), salt=salt, n=2**14, r=8, p=1).hex()
def attack(target, fn):
    start = time.perf_counter(); tried = 0
    for w in WORDLIST:
        tried += 1
        if fn(w) == target: return w, tried, time.perf_counter() - start
    return None, tried, time.perf_counter() - start
def main():
    rows = []
    for pw in TEST_PASSWORDS:
        salt = os.urandom(16)
        for name, h, fn in (("MD5, no salt", md5(pw), md5),
                            ("SHA-256 + salt", sha256_salted(pw, salt), lambda w: sha256_salted(w, salt)),
                            ("scrypt + salt", scrypt(pw, salt), lambda w: scrypt(w, salt))):
            found, tried, secs = attack(h, fn); rows.append((pw, name, found, tried, secs))
            print(f"{pw:30} {name:16} {'CRACKED: ' + found if found else 'not found':22} tried {tried:2}  {secs * 1000:8.2f} ms")
    return rows
if __name__ == "__main__":
    main()
