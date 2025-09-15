# Contributing to Docling Parser

We welcome contributions to the Docling Parser project! This document provides guidelines for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/docling-parser.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Commit your changes: `git commit -am 'Add some feature'`
6. Push to the branch: `git push origin feature/your-feature-name`
7. Create a new Pull Request

## Development Setup

1. Install dependencies: `uv sync`
2. Run tests: `pytest`
3. Format code: `black .` and `isort .`
4. Check code style: `flake8`

## Code Style

We follow the standard Python PEP 8 style guide with some modifications:

- Line length: 88 characters (following Black's default)
- Use type hints where possible
- Write docstrings for all public functions and classes
- Keep functions small and focused
- Use meaningful variable names

## Commit Message Guidelines

We follow the Conventional Commits specification to ensure consistency and enable automated changelog generation.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to our CI configuration files and scripts
- `chore`: Other changes that don't modify src or test files
- `revert`: Reverts a previous commit

### Scope

Specify a scope to indicate the area of the codebase that was affected. Examples:

- `parser`
- `cli`
- `docs`
- `tests`
- `config`

### Subject

- Use imperative, present tense: "change" not "changed" nor "changes"
- Don't capitalize the first letter
- No dot (.) at the end

### Body

- Just as in the subject, use the imperative, present tense
- Wrap at 72 characters
- Explain the "what" and "why", not "how"

### Footer

- Reference issues that this commit closes
- Use "Fixes: #123" or "Closes: #123"

### Examples

```
feat(parser): add support for concurrent document processing

- Implement ThreadPoolExecutor for parallel document parsing
- Add --concurrent flag to advanced_parsing.py
- Add --max-workers option to control concurrency level

Fixes: #45
```

```
docs(readme): update usage instructions

- Add section about concurrent parsing options
- Clarify environment variable setup
- Update example commands

Closes: #67
```

You can also use the commit template provided in `.github/commit_message_template.txt` to help you format your commit messages.

### Commit Message Validation

We have two levels of commit message validation:

1. **Local Validation**: Git commit hooks that run on your local machine when you make commits
2. **Server Validation**: GitHub Actions that validate all commits in pull requests

To set up local validation:

- On Unix-like systems: Run `.github/setup_commit_hooks.sh`
- On Windows: Run `.github/setup_commit_hooks.ps1`

The server validation automatically runs on all pull requests and will prevent merging if any commit messages don't follow the Conventional Commits specification.

## Testing

- Write tests for new functionality
- Ensure all tests pass before submitting a pull request
- Aim for high test coverage
- Test edge cases and error conditions

## Documentation

- Update documentation when adding new features
- Write clear, concise docstrings
- Update README.md if necessary
- Add examples for new functionality

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build
2. Update the README.md with details of changes to the interface
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent
4. Your Pull Request will be reviewed by maintainers, who may request changes
5. Once approved, your Pull Request will be merged

## Reporting Issues

- Use the GitHub issue tracker to report bugs
- Describe the issue clearly
- Include steps to reproduce
- Specify your environment (Python version, OS, etc.)
- Include any relevant error messages or logs

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.
