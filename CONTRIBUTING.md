# Contributing to LinkedIn Skills Semantic Transformer

Thank you for your interest in contributing to this project! Here are some guidelines to help you get started.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with the following information:
- A clear, descriptive title
- A detailed description of the bug
- Steps to reproduce the behavior
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are always welcome! Please create an issue with:
- A clear, descriptive title
- A detailed description of the enhancement
- Why this enhancement would be useful
- Possible implementation approaches (if you have ideas)

### Submitting Pull Requests

1. **Fork the repository** and create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Set up your development environment:**
   ```bash
   poetry install --with dev
   ```

3. **Make your changes** and commit with clear, concise commit messages:
   ```bash
   git commit -m "Add feature: description of changes"
   ```

4. **Ensure code quality:**
   - Write or update tests for your changes
   - Run the test suite: `pytest tests/ -v`
   - Ensure your code follows the project's style guidelines
   - Type hints are appreciated

5. **Push to your fork and submit a pull request:**
   - Provide a clear description of your changes
   - Reference any related issues
   - Ensure all tests pass

## Code Style Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and maintainable
- Add comments for complex logic

## Testing

- Write tests for new features
- Ensure all existing tests pass before submitting a PR
- Aim for reasonable code coverage

Run tests with:
```bash
pytest tests/ -v
```

## Project Structure

The project is organized as follows:
- `src/linkedin_skill_semantic_transformer/` - Main package code
- `tests/` - Test suite
- `pyproject.toml` - Project configuration and dependencies

## Questions?

Feel free to open an issue to ask questions or discuss ideas. We're here to help!

## License

By contributing, you agree that your contributions will be licensed under the MIT License (see the LICENSE file in the repository).

---

Thank you for contributing!
