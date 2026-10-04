"""passaudit - a simple password strength auditor."""

import math
import string


def charset_size(password: str) -> int:
    """Return how many possible characters the password draws from."""
    size = 0
    if any(c.islower() for c in password):
        size += 26
    if any(c.isupper() for c in password):
        size += 26
    if any(c.isdigit() for c in password):
        size += 10
    if any(c in string.punctuation for c in password):
        size += len(string.punctuation)
    return size


def entropy_bits(password: str) -> float:
    """Estimate password entropy in bits."""
    size = charset_size(password)
    if size == 0 or len(password) == 0:
        return 0.0
    return len(password) * math.log2(size)


def find_issues(password: str) -> list[str]:
    """Return a list of problems with the password."""
    issues = []
    if len(password) < 12:
        issues.append("Too short (use at least 12 characters)")
    if not any(c.islower() for c in password):
        issues.append("No lowercase letters")
    if not any(c.isupper() for c in password):
        issues.append("No uppercase letters")
    if not any(c.isdigit() for c in password):
        issues.append("No digits")
    if not any(c in string.punctuation for c in password):
        issues.append("No symbols")
    if len(set(password)) < 5:
        issues.append("Too repetitive")
    return issues


def rate(bits: float) -> str:
    if bits < 40:
        return "WEAK"
    if bits < 60:
        return "MODERATE"
    if bits < 80:
        return "STRONG"
    return "VERY STRONG"


def audit(password: str) -> None:
    bits = entropy_bits(password)
    issues = find_issues(password)
    print("-" * 40)
    print(f"Length:   {len(password)}")
    print(f"Entropy:  {bits:.1f} bits")
    print(f"Rating:   {rate(bits)}")
    if issues:
        print("Issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("No issues found.")
    print("-" * 40)


def main() -> None:

    import sys

    if len(sys.argv) > 1:
        # Command-line mode: passaudit <password>
        audit(sys.argv[1])
        return

    #Interactive mode
    print("passaudit v0.1 - type 'quit' to exit")
    while True:
        pw = input("Enter a password to audit: ")
        if pw.lower() == "quit":
            break
        audit(pw)


if __name__ == "__main__":
    main()





