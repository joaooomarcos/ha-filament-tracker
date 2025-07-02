# CONTRIBUTING.md

## Contributing to Filament Tracker for Home Assistant

Thank you for your interest in contributing to the Filament Tracker integration for Home Assistant!  
We welcome all contributions, whether they are bug reports, feature requests, code improvements, or documentation updates.

---

## Getting Started

1. **Fork the repository**  
   Click the "Fork" button at the top right of this page to create your own copy of the repository.

2. **Clone your fork**  
   ```bash
   git clone https://github.com/<your-username>/ha_core.git
   cd ha_core
   ```

3. **Set up the development environment**  
   - Use the provided devcontainer or set up Python 3.13 and Home Assistant Core dependencies.
   - Install requirements:
     ```bash
     pip install -r requirements.txt
     ```

4. **Create a new branch**  
   ```bash
   git checkout -b my-feature-or-fix
   ```

---

## Code Style & Quality

- **Python 3.13** features are encouraged (pattern matching, type hints, dataclasses, etc).
- Use [Ruff](https://docs.astral.sh/ruff/) for formatting and linting.
- Run [PyLint](https://pylint.org/) and [MyPy](http://mypy-lang.org/) for static analysis and type checking.
- Write clear docstrings for all functions and classes.
- Follow the Home Assistant [architecture](https://developers.home-assistant.io/docs/architecture_index/) and [integration structure](https://developers.home-assistant.io/docs/integration_setup_index/).

---

## Making Changes

- Keep pull requests focused and atomic.
- Reference related issues in your PR description (e.g., `Closes #123`).
- Add or update tests in `tests/components/filament_tracker/` as needed.
- Ensure all tests pass before submitting:
  ```bash
  pytest tests/components/filament_tracker/
  ```

---

## Commit Messages

- Use clear, descriptive commit messages.
- Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) style if possible.

---

## Pull Request Process

1. **Push your branch** to your fork.
2. **Open a pull request** against the `main` branch of this repository.
3. The maintainers will review your PR and may request changes.
4. Once approved, your PR will be merged.

---

## Reporting Issues

- Use [GitHub Issues](https://github.com/joaooo_marcos/ha_core/issues) to report bugs or request features.
- Please provide as much detail as possible, including logs, configuration, and steps to reproduce.

---

## Code of Conduct

Be respectful and inclusive. All interactions in this project are governed by the [Home Assistant Code of Conduct](https://www.home-assistant.io/code_of_conduct/).

---

Thank you for helping make

This text was generated using artificial intelligence.