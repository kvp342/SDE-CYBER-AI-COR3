# Password storage

## Never store plain text
Store only a hash of each password, never the password itself and never reversible encryption.

## Use a slow hash
Use a slow, salted password hashing function such as Argon2id, bcrypt or scrypt. Fast hashes like MD5 or SHA-256 alone are easy to brute-force with GPUs.

## Salt
A salt is a random value stored with each hash. It makes identical passwords produce different hashes and defeats precomputed rainbow tables.

## Login protection
Rate-limit login attempts and support multi-factor authentication. Compare hashes in constant time.
