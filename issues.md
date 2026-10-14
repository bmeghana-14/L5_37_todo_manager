# Lab 5: Static Code Analysis — Issue Log

## Objective

To identify and fix code-quality, security, and style issues in `todo_manager.py` using Pylint, Bandit, and Flake8.

## Issues Identified and Fixes Applied

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Shell command injection | Security — High | 57 | `os.system()` combined a shell command with an email address, potentially allowing command injection. | Replaced shell execution with Python's email and SMTP APIs. |
| Unsafe pickle deserialization | Security — Medium | 47 | `pickle.load()` can execute malicious code when processing an untrusted pickle file. | Replaced pickle persistence with JSON and added basic data validation. |
| Mutable default argument | Code quality | 11 | `labels=[]` could reuse the same mutable list across function calls. | Changed the default to `None` and initialized a fresh list for each call. |
| Inconsistent naming | Style | Multiple | CamelCase function and variable names did not follow the recommended snake_case convention. | Renamed functions and variables to snake_case. |
| Missing docstrings | Maintainability | Multiple | The module and functions lacked documentation. | Added a module docstring and function docstrings. |
| Missing encoding | Code quality | 51 | A text file was opened without explicitly specifying an encoding. | Specified UTF-8 when opening JSON files. |
| Inconsistent return statements | Code quality | 33 | The search function implicitly returned `None` when no match was found. | Made the return behavior explicit and added a return type annotation. |
| Formatting violations | Style | Multiple | Flake8 identified spacing and blank-line violations. | Corrected whitespace and formatting. |
| Insecure random selection warning | Security analysis | 70 | Bandit flagged `random.choice()` because the standard pseudo-random generator is unsuitable for security-sensitive selection. | Replaced it with `secrets.choice()` for secure random selection. |

## Verification

The original analysis reported a Pylint score of 5.09/10, four Bandit findings, and four Flake8 violations.

The revised code was analyzed again using all three tools. Final scores and remaining findings should be recorded from the saved `pylint_report_after.txt`, `bandit_report_after.txt`, and `flake8_report_after.txt` files.