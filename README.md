# Passgen Toolkit

A lightweight Python library for generating and validating passwords, built on Python's standard `secrets` module (cryptographically secure randomness).

It provides secure random integers, general-purpose password generators, a generator for common website-style rules, wrapper passwords around your own text, and an experimental multilingual generator.

## Features

- **Secure random integers**: `secrandint()` is a secure replacement for `random.randint`.
- **Secure shuffle**: `secure_shuffle()` uses the Fisher-Yates algorithm driven by `secrandint()`.
- **Core generator**: `gen_pass()` builds passwords from letters, digits and symbols, with optional exact counts of each.
- **Rule-compliant generator**: `valpasgen()` always satisfies the custom rules checked by `val_pass()`.
- **Validators**: `validate_string()` and `val_pass()` check which character types a password contains and whether it meets a common website-style rule set.
- **Custom wrapper passwords**: `cpasgen()` pads your own text and number with random punctuation.
- **Multilingual passwords (experimental)**: `langpass()` picks letters from many writing systems (Cyrillic, Arabic, Korean, Chinese, Tamil, Hindi, Greek and more).

## Installation

No external dependencies. Requires Python 3.6+ (for `secrets` and f-strings).

1. Place `passgen.py` in your project folder.
2. Import it:

```python
from passgen import *
# or
import passgen
```

## Quick-Start Reference

### 1. Randomness and shuffling

#### `secrandint(a, b)`

Returns a cryptographically secure random integer between `a` and `b` (both inclusive). Raises `ValueError` if `a > b`.

```python
num = secrandint(1, 100)
```

#### `secure_shuffle(text)`

Returns the characters of `text` in a random order (Fisher-Yates shuffle using `secrandint()`).

```python
shuffled = secure_shuffle("Password123")
```

### 2. Password generators

#### `gen_pass(l=12, d=())`

Generates a password of length `l` using letters, digits and symbols.

Note that in the default mode the password is not guaranteed to contain every character type. For guaranteed composition, pass a tuple `d = (digits, letters, symbols)` with exact counts. When `d` is given, `l` is ignored and the length is the sum of the tuple.

```python
p1 = gen_pass()                  # 12 random characters
p2 = gen_pass(16)                # 16 random characters
p3 = gen_pass(d=(2, 8, 2))       # exactly 2 digits, 8 letters, 2 symbols (length 12)
```

#### `chrgen(l=12)`

Generates `l` random characters from the printable ASCII range (character codes 33 to 126).

```python
raw_ascii = chrgen(16)
```

#### `valpasgen(l=12)`

Generates a password that always satisfies the rules in `val_pass()` below. `l` must be at least 8, otherwise `ValueError` is raised.

```python
policy_pass = valpasgen(16)
```

### 3. Validation

#### `validate_string(text)`

Returns a tuple `(has_lowercase, has_digit, has_uppercase)` of booleans.

```python
validate_string("abcD1")   # (True, True, True)
```

#### `val_pass(text)`

Returns `True` if the text meets this custom, website-style rule set:

- at least 8 characters
- at least 1 lowercase letter
- at least 1 uppercase letter
- at least 1 digit
- at least 1 space
- at least 1 symbol from `! @ # $ % _ -`

> **Note:** This is a common style of website rule, not a NIST recommendation. NIST guidance (SP 800-63B) favors length and checking against breached-password lists over forced character-type rules.

### 4. Custom and multilingual generators

#### `cpasgen(l, s, n, o=None)`

Wraps your own text `s` and number `n` with random punctuation to reach total length `l`. If `o` is omitted, the function asks which mode to use.

| `o` | Result |
|-----|--------|
| `1` | `s` + random punctuation + `n` |
| `2` | all of the above shuffled together |
| `3` | random punctuation + `s` + `n` |
| `0` | prints all three versions and returns `None` |

Any other value raises `ValueError`.

```python
cpasgen(16, "hello", 2024, 2)
```

> **Warning:** Only the random punctuation is secret. Text and numbers you add (names, birth years) are guessable, so keep `l` much larger than `len(s) + len(n)` and avoid personal information.

#### `langpass(l, lan=None)`

Generates a password of length `l` (minimum 8) made of 2 digits, 1 symbol, and letters picked from the chosen writing systems, all shuffled together. Only real letters are used (unassigned and combining Unicode characters are filtered out).

`lan` is a list of language names from `Lang_range`. If omitted, all languages are used. Unknown names raise `ValueError`.

```python
global_token = langpass(16, ['latin', 'korean', 'hindi', 'tamil', 'chinese'])
default_token = langpass(12)
```

Strength depends on the languages you choose. Many languages give high entropy, while `['latin']` alone gives only the 26 uppercase letters A to Z.

> **Use with caution:**
> - Many websites reject non-ASCII passwords.
> - Unicode normalization differences can make the same password fail on another device.
> - bcrypt only reads the first 72 bytes, and CJK characters take 3 bytes each, so long passwords may be silently truncated.
> - You will almost certainly need a password manager to enter them.

## Customizing the language list

`Lang_range` maps a language name to a range of Unicode code points:

```python
Lang_range = {
    "cyrillic": (0x0410, 0x044F),
    "arabic": (0x0621, 0x064A),
    "korean": (0xAC00, 0xD7A3),
    "chinese": (0x4E00, 0x9FA5),
    "latin": (0x0041, 0x005A),
    "hiragana": (0x3040, 0x309F),
    "thai": (0x0E00, 0x0E7F),
    "hindi": (0x0900, 0x097F),
    "tamil": (0x0B80, 0x0BFF),
    "tibetan": (0x0F00, 0x0FFF),
    "sinhala": (0x0D80, 0x0DFF),
    "georgian": (0x10A0, 0x10FF),
    "ethiopic": (0x1200, 0x137F),
    "telugu": (0x0C00, 0x0C7F),
    "gujarati": (0x0A80, 0x0AFF),
    "punjabi": (0x0A00, 0x0A7F),
    "greek": (0x0370, 0x03FF),
}
```

To add or remove languages, edit this dictionary **in `passgen.py`**. The `POOLS` table (the letters actually used) is built from it when the module loads, so adding an entry to `Lang_range` at runtime will cause a `KeyError`.

## Disclaimer

This software is provided "as is", without warranty of any kind. Although Passgen uses the cryptographically secure `secrets` module, security is a system-wide practice. The authors are not responsible for compromised accounts, data breaches, or security vulnerabilities resulting from its use. Always use proper password hashing (for example Argon2 or bcrypt), secure transmission (HTTPS) and safe storage, and avoid reusing passwords across sites.
