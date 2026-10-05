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
def audit_file(path: str) -> None:
    """Read passwords from a file, one per line, and report the weakest."""
    try:
        with open(path) as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: file not found: {path}")
        return
    except PermissionError:
        print(f"Error: no permission to read: {path}")
        return

    if not passwords:
        print("No passwords in file.")
        return

    results = []
    for pw in passwords:
        bits = entropy_bits(pw)
        results.append((bits, pw))

    results.sort()  # weakest first

    print(f"Audited {len(results)} passwords from {path}")
    print("Weakest 5:")
    for bits, pw in results[:5]:
        rating = rate(bits)
        display = pw if len(pw) <= 20 else pw[:20] + "..."
        print(f"  [{rating:11}] {bits:6.1f} bits  {display}")


def main() -> None:
    import sys

    if len(sys.argv) > 2 and sys.argv[1] == "--file":
        audit_file(sys.argv[2])
        return

    if len(sys.argv) > 1:
        audit(sys.argv[1])
        return

    print("passaudit v0.2 - type 'quit' to exit")
    print("Usage: passaudit <password>  OR  passaudit --file <path>")
    while True:
        try:
            pw = input("Enter a password to audit: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if pw.lower() == "quit":
            break
        audit(pw)


if __name__ == "__main__":
    main()
