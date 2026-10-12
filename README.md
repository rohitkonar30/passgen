# Passgen Toolkit 

A lightweight, cryptographically secure Python password generation and validation library built on top of Python's built-in `secrets` module. 

Designed for developers who need secure random integers, compliant random strings, and customizable wrapper passwords.

---

## Features

- **Secure Random Integers:** `secrandint()` acts as a secure alternative to `random.randint`.
- **Core Generator:** `gen_pass()` builds robust passwords mixing letters, digits, and symbols.
- **Compliance Checks:** Validate passwords against robust character rules and checks for compliance with NIST regulations (`validate_string` and `val_Nist`).
- **Custom password Generator:** `cpasgen()` lets you embed custom strings and numbers into automatically padded secure tokens.

---
## Disclaimer

This software is provided "as is", without warranty of any kind. While `passgen` uses cryptographically secure pseudo-random number generators (`secrets`), security is a system-wide practice. 
The authors are not responsible for any compromised accounts, data breaches, or security vulnerabilities resulting from the use of this library.
Always ensure proper password hashing (e.g., Argon2, bcrypt), secure transmission (HTTPS), and safe storage practices in your applications.

## Installation

To use this module in your project, simply place `passgen.py` in your project directory and import it
**Requirements:** It has **no external dependencies** and is a lightweight module.
