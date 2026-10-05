"""Basic tests for passaudit entropy calculation."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from passaudit import entropy_bits, find_issues, rate


def test_empty_password():
    assert entropy_bits("") == 0.0


def test_weak_password():
    assert rate(entropy_bits("hello")) == "WEAK"


def test_strong_password():
    bits = entropy_bits("Tr0ub4dor&3xYz!")
    assert bits > 80


def test_short_password_flagged():
    issues = find_issues("abc")
    assert "Too short (use at least 12 characters)" in issues


if __name__ == "__main__":
    test_empty_password()
    test_weak_password()
    test_strong_password()
    test_short_password_flagged()
    print("All tests passed.")
