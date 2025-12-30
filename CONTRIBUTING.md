# Contributing to TurboLightDI

First off, thank you for considering contributing to **TurboLightDI**!

Please take a moment to review these guidelines to make the contribution process easy and effective for everyone involved.

---

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and inclusive in all interactions.

## How Can I Contribute?

### 1. Reporting Bugs
* **Check the Issue Tracker:** See if the bug has already been reported.
* **Use a Template:** If it's a new bug, open an issue using the bug report template.
* **Be Specific:** Include steps to reproduce, the expected behavior, and the actual behavior.

### 2. Suggesting Enhancements
* Explain the "why" behind the feature.
* Provide examples of how the new API or functionality would look.
* Check existing issues to ensure the idea hasn't been proposed or rejected already.

### 3. Pull Requests
* **Branching:** Create a new branch for every feature or bug fix (`feature/your-feature-name` or `bugfix/issue-id`).
* **Atomic Commits:** Keep commits small and focused on a single change.
* **Tests:** Ensure that existing tests pass and add new tests for any new functionality.
* **Documentation:** Update the `README.md` or other relevant docs if you change any public APIs.

---

## Development Setup

1.  **Fork the Repository:** Create your own fork of the project.
2.  **Clone Locally:**
    ```bash
    git clone [https://github.com/turborg/turbolightdi.git](https://github.com/turborg/turbolightdi.git)
    cd turbolightdi
    ```
3.  **Install Dependencies:**
We use `uv` for lightning-fast dependency management and project isolation.
    ```bash
    uv sync --extra dev
    ```
4.  **Run Tests:**
    ```bash
    pytest
    ```

---

## Coding Standards

* Follow the standard naming conventions for the language (check pre-commit-config.yaml for more)
* Maintain a clean, readable style.
* Avoid adding unnecessary external dependencies.

## Style Guide for Commits

We follow a basic conventional commit format:
* `feat:` A new feature
* `fix:` A bug fix
* `docs:` Documentation only changes
* `refactor:` A code change that neither fixes a bug nor adds a feature

---

## Questions?

If you have any questions, feel free to open a discussion or an issue labeled `question`. We’re happy to help!

**Thank you for your contribution!**

---
*Part of the [**Turborg**](https://turborg.com) AI-First Open Source Suite Ecosystem*
