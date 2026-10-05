# passaudit

A Python CLI that scores password strength using entropy estimation.

## Install

```bash
pip install -e .
# Audit a single password
passaudit "Tr0ub4dor&3xYz!"

# Audit a file of passwords (one per line)
passaudit --file wordlist.txt

# Interactive mode
passaudit
