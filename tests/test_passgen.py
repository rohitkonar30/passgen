"""Tests for passgen, written from the behaviour the README promises.

If a test fails, one of two things is true: the code has a bug, or the README
is wrong. Decide which, fix it, and keep the test. Run from the repo root with:

    python -m pytest -q
"""
import ast
from collections import Counter
from pathlib import Path
import string

import pytest

import passgen as pg

ALNUM = set(string.ascii_letters + string.digits)


# --- randomness and shuffling -------------------------------------------------

def test_secrandint_stays_in_range_and_is_inclusive():
    seen = {pg.secrandint(2, 4) for _ in range(500)}
    assert seen == {2, 3, 4}


def test_secrandint_rejects_reversed_bounds():
    with pytest.raises(ValueError):
        pg.secrandint(5, 1)


def test_secure_shuffle_keeps_the_same_characters():
    text = "Password123"
    out = pg.secure_shuffle(text)
    assert len(out) == len(text)
    assert Counter(out) == Counter(text)


def test_secure_shuffle_actually_reorders():
    outputs = {pg.secure_shuffle("abcdefgh") for _ in range(50)}
    assert len(outputs) > 1


# --- generators ---------------------------------------------------------------

def test_gen_pass_default_and_custom_length():
    assert len(pg.gen_pass()) == 12
    assert len(pg.gen_pass(16)) == 16


def test_gen_pass_exact_counts():
    for _ in range(50):
        p = pg.gen_pass(d=(2, 8, 2))
        assert len(p) == 12
        assert sum(c in string.digits for c in p) == 2
        assert sum(c in string.ascii_letters for c in p) == 8
        assert sum(c not in ALNUM for c in p) == 2


def test_chrgen_uses_printable_ascii_only():
    p = pg.chrgen(200)
    assert len(p) == 200
    assert all(33 <= ord(c) <= 126 for c in p)


@pytest.mark.parametrize("length", [8, 12, 20])
def test_valpasgen_always_passes_val_pass(length):
    for _ in range(100):
        p = pg.valpasgen(length)
        assert len(p) == length
        assert pg.val_pass(p)


def test_valpasgen_rejects_short_length():
    with pytest.raises(ValueError):
        pg.valpasgen(7)


# --- validators ---------------------------------------------------------------

@pytest.mark.parametrize(
    "text, expected",
    [
        ("abcD1", (True, True, True)),
        ("abc", (True, False, False)),
        ("ABC", (False, False, True)),
        ("123", (False, True, False)),
    ],
)
def test_validate_string(text, expected):
    # order per README: (has_lowercase, has_digit, has_uppercase)
    assert pg.validate_string(text) == expected


def test_val_pass_accepts_a_compliant_password():
    assert pg.val_pass("Abcde1 !x")


@pytest.mark.parametrize(
    "bad",
    [
        "Ab1 !",        # too short
        "abcde1 !x",    # no uppercase
        "ABCDE1 !X",    # no lowercase
        "Abcdef !x",    # no digit
        "Abcde1!xy",    # no space
        "Abcde1 xyz",   # no allowed symbol
    ],
)
def test_val_pass_rejects_each_missing_rule(bad):
    assert not pg.val_pass(bad)


# --- custom and multilingual generators ---------------------------------------

def test_cpasgen_mode_1_text_first_number_last():
    p = pg.cpasgen(16, "hello", 2024, 1)
    assert len(p) == 16
    assert p.startswith("hello")
    assert p.endswith("2024")


def test_cpasgen_mode_3_punctuation_first():
    p = pg.cpasgen(16, "hello", 2024, 3)
    assert len(p) == 16
    assert p.endswith("hello2024")


def test_cpasgen_mode_2_keeps_all_your_characters():
    p = pg.cpasgen(16, "hello", 2024, 2)
    assert len(p) == 16
    assert not (Counter("hello2024") - Counter(p))


def test_cpasgen_mode_0_prints_and_returns_none(capsys):
    assert pg.cpasgen(16, "hello", 2024, 0) is None
    assert capsys.readouterr().out.strip()


def test_cpasgen_rejects_unknown_mode():
    with pytest.raises(ValueError):
        pg.cpasgen(16, "hello", 2024, 9)


def test_langpass_length_and_digits():
    p = pg.langpass(12)
    assert len(p) == 12
    assert sum(c.isdigit() for c in p) >= 2


def test_langpass_latin_only_uses_uppercase_letters():
    p = pg.langpass(16, ["latin"])
    letters = [c for c in p if c.isalpha()]
    assert letters
    assert all(c in string.ascii_uppercase for c in letters)


def test_langpass_rejects_short_length_and_unknown_language():
    with pytest.raises(ValueError):
        pg.langpass(7)
    with pytest.raises(ValueError):
        pg.langpass(12, ["klingon"])


def test_lang_range_entries_are_valid_ranges():
    for name, (low, high) in pg.Lang_range.items():
        assert low <= high, name


# --- the security claim itself ------------------------------------------------

def test_module_never_imports_random():
    """README says randomness comes from `secrets`; fail if `random` sneaks in."""
    tree = ast.parse(Path(pg.__file__).read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert "random" not in imported
    assert "secrets" in imported


# --- issues found in review (these fail until the code is fixed) ---------------

def test_valpasgen_never_puts_the_space_at_either_end():
    """Many login forms trim whitespace, so a leading/trailing space breaks the password."""
    for _ in range(300):
        p = pg.valpasgen(12)
        assert p[0] != " " and p[-1] != " "


def test_cpasgen_rejects_text_that_does_not_fit_in_length():
    with pytest.raises(ValueError):
        pg.cpasgen(8, "hello", 2024, 1)
