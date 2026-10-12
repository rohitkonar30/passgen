# Passgen Toolkit 

A lightweight, cryptographically secure Python password generation and validation library built on top of Python's built-in `secrets` module. 

Designed for developers who need secure random integers, compliant random strings, and customizable wrapper passwords.

---

## Features

- **Secure Random Integers:** `secrandint()` acts as a secure alternative to `random.randint`.
- **Core Generator:** `gen_pass()` builds robust passwords mixing letters, digits, and symbols.
- **Compliance Checks:** Validate passwords against robust character rules and checks for compliance with widely accepted regulations (`validate_string()` and `val_pass()`).
- **Custom password Generator:** `cpasgen()` lets you embed custom strings and numbers into automatically padded secure tokens.
- **Secure Shuffle**: It implements a robust Fisher-Yates shuffling algorithm to safely mix custom tokens and character sets using `secrandint()`.
- **Multilingual Unicode Blocks**: It supports global character blocks including Cyrillic, Arabic, Korean, Chinese, Tamil, Hindi, Greek, and more.

## Quick-Start Reference Guide

### 1. Core Randomness & Shuffling

* **`secrandint(a, b)`**
  * **What it does:** Generates a cryptographically secure random integer between `a` and `b` (inclusive).
  * **Example:**
    ```python
    num = secrandint(1, 100)
    ```

* **`secure_shuffle(text)`**
  * **What it does:** Randomly shuffles the characters of a string using the Fisher-Yates algorithm using `secrandint()`.
  * **Example:**
    ```python
    shuffled = secure_shuffle("Password123")
    ```

---

### 2. Password Generators

* **`gen_pass(l=12, d=())`**
  * **What it does:** Generates a secure password of length `l`. Passing a tuple `(digits, alphabets, specials)` specifies exact composition counts.
  * **Example:**
    ```python
    # Custom composition: 2 digits, 8 letters, 2 specials
    p = gen_pass(l=12, d=(2, 8, 2))
    ```

* **`chrgen(l=12)`**
  * **What it does:** Generates a raw secure random sequence using standard printable ASCII character codes (decimal 33 to 126).
  * **Example:**
    ```python
    raw_ascii = chrgen(16)
    ```

* **`valpassgen(l=12)`**
  * **What it does:** Continuously generates ASCII strings using the `pass_gen()` framework and passes strictly according to custom standards.
  * inclusion of 1 space
  * inclusion of 1 uppercase
  * inclusion of 1 lowercase
  * inclusion of 1 special character
  * minimum of 8 characters
  * **Example:**
    ```python
    nist_pass = Nipasgen(16)
    ```

---

### 3. Validation Functions

* **`validate_string(text)`**
  * **What it does:** Checks a string and returns a tuple indicating the presence of lowercase letters, digits, and uppercase letters `(lo, di, up)`.

* **`val_pass(text)`**
  * **What it does:** Validates whether a string meets specific custom standards still widely adopted in websites.
  These include:
  * inclusion of 1 space
  * inclusion of 1 uppercase
  * inclusion of 1 lowercase
  * inclusion of 1 special character
  * minimum of 8 characters 

---

### 4. Custom & Multilingual Generators

* **`cpasgen(l, s, n, o=None)`**
  * **What it does:** Combines user-defined string fragments (`s`), numbers/strings (`n`), and punctuation to create customized password structures. `o` bypasses the user input prompt needed for the different formats as it is predefined by the value of o.
  * o=1:
    it refers to the string text to be at the start followed by the special characters and then the custom numbers.
  * o=2:
    it refers to completely scramble the secure password created by the above combination.
  * o=3:
    it refers the special characters at the start of the text and then followed by the text and numerals    

* **`langpass(l, lan:list=None)`**
  * **What it does:** Generates a high-entropy password combining ASCII prefixes with characters picked randomly from global Unicode language blocks (e.g., Cyrillic, Arabic, Korean, Tamil, Greek, etc.).
  * **Example:**
    ```python
    global_token = langpass(16,['latin','korean','hindi','tamil','chinese'])
    ```
    The default value go the lan list is the `Lang_rang` which contains a select language and can be modified to ones choice.
    `Lang_range = {
    "cyrillic": (0x0410, 0x044F),
    "arabic": (0x0621, 0x064A),
    "korean": (0xAC00, 0xD7A3),
    "chinese": (0x4E00, 0x9FA5),
    "latin": (0x0041, 0x005A),
    'hiragana': (0x3040, 0x309F),
    "thai": (0x0E00, 0x0E7F),
    "hindi":(0x0900, 0x097F),
    "tamil": (0x0B80, 0x0BFF),
    "tibetan": (0x0F00, 0x0FFF),
    "sinhala": (0x0D80, 0x0DFF),
    "georgian": (0x10A0, 0x10FF),
    "ethiopic": (0x1200, 0x137F),
    "telugu": (0x0C00, 0x0C7F),
    "gujarati": (0x0A80, 0x0AFF),
    "punjabi": (0x0A00, 0x0A7F),
    "greek": (0x0370, 0x03FF)
}`
---
## Disclaimer

This software is provided "as is", without warranty of any kind. While `passgen` uses cryptographically secure pseudo-random number generators (`secrets`), security is a system-wide practice. 
The authors are not responsible for any compromised accounts, data breaches, or security vulnerabilities resulting from the use of this library.
Always ensure proper password hashing (e.g., Argon2, bcrypt), secure transmission (HTTPS), and safe storage practices in your applications.

## Installation

To use this module in your project, simply place `passgen.py` in your project directory and import it
**Requirements:** It has **no external dependencies** and is a lightweight module.
