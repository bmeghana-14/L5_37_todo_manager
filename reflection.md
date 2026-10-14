# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, maintainability problems, and coding-standard violations early in development. This allows developers to improve software quality before deployment.

## 2. What did Pylint, Bandit, and Flake8 detect?

Pylint identified code-quality issues such as missing docstrings, inconsistent naming, a mutable default argument, and inconsistent return statements. Bandit identified unsafe pickle deserialization and shell command construction, along with a warning about standard pseudo-random selection. Flake8 identified spacing and formatting violations.

## 3. Which issues did you fix, and how did you verify the fixes?

I corrected the mutable default argument, replaced pickle-based persistence with JSON, removed shell command construction from the email helper, improved naming and documentation, specified file encodings, and corrected formatting. I reran Pylint, Bandit, and Flake8 and executed the program to check that its task-management functionality still worked.

The final reports provide evidence of which findings were resolved and whether any warnings remain.

## 4. How does static analysis improve code quality and security?

Static analysis makes code reviews more systematic by detecting common problems consistently. Pylint focuses on code quality and maintainability, Bandit checks for common security weaknesses, and Flake8 checks style and formatting. Using all three provides complementary coverage. Static analysis does not replace runtime testing or manual code review, but it helps detect problems before software is deployed.