# Document Parsing with Docling

This project demonstrates how to parse documents using the Docling library.

## Features

- Parse various document formats (PDF, DOCX, PPTX, images, etc.)
- Export documents to Markdown, HTML, JSON, and other formats
- Customizable parsing options
- Batch processing capabilities
- Concurrent processing support

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

## Setup

### Using uv (recommended)

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd docling-parser
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

### Using pip

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd docling-parser
   ```

2. Create and activate a virtual environment:

   ```bash
   yv venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Environment Variables

Some dependencies may require environment variables to be set. To simplify this process, we provide scripts to set them:

On Windows (Command Prompt):

```cmd
run_parser.bat
```

On Windows (PowerShell):

```powershell
.\run_parser.ps1
```

On Unix-like systems (macOS, Linux):

```bash
# First make the script executable (only needed once)
chmod +x run_parser.sh
./run_parser.sh
```

You can also pass arguments to these scripts:

```cmd
run_parser.bat "path/to/document.pdf" -o "output/result.md"
```

Or run the scripts directly with Python (environment variables will still be set automatically):

```bash
python parse_document.py
```

## Usage

### Command Line Interface

```bash
parse-doc
```

### Python Scripts

Run the basic parsing example:

```bash
python parse_document.py
```

Run the advanced parsing example with concurrent processing:

```bash
python advanced_parsing.py --concurrent --max-workers 8 doc1.pdf doc2.pdf doc3.pdf
```

### As a Library

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("path/to/document.pdf")
markdown_content = result.document.export_to_markdown()
```

## Development Tasks

This project includes a Makefile for common development tasks. On Unix-like systems (macOS, Linux), you can use:

```bash
make help      # Show available targets
make sync      # Install dependencies
make format    # Format code
make lint      # Check code style
make test      # Run tests
make clean     # Clean up generated files
```

On Windows, use the PowerShell script instead:

```powershell
.\Makefile.ps1 help      # Show available targets
.\Makefile.ps1 sync      # Install dependencies
.\Makefile.ps1 format    # Format code
.\Makefile.ps1 lint      # Check code style
.\Makefile.ps1 test      # Run tests
.\Makefile.ps1 clean     # Clean up generated files
```

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
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to our CI configuration files and scripts
- `chore`: Other changes that don't modify src or test files
- `revert`: Reverts a previous commit

### Commit Validation

We have two levels of commit message validation:

1. **Local Validation**: Git commit hooks that run on your local machine when you make commits
2. **Server Validation**: GitHub Actions that validate all commits in pull requests

To set up local validation:

- On Unix-like systems: Run `.github/setup_commit_hooks.sh`
- On Windows: Run `.github/setup_commit_hooks.ps1`

The server validation automatically runs on all pull requests and will prevent merging if any commit messages don't follow the Conventional Commits specification.

## Project Structure

```
docling-parser/
├── parse_document.py          # Basic document parsing example
├── advanced_parsing.py        # Advanced parsing examples
├── run_parser.bat             # Run parser with env vars (Windows)
├── run_parser.ps1             # Run parser with env vars (PowerShell)
├── run_parser.sh              # Run parser with env vars (Unix/macOS)
├── set_env_vars.bat           # Set environment variables (Windows)
├── set_env_vars.ps1           # Set environment variables (PowerShell)
├── Makefile                   # Development tasks (Unix)
├── Makefile.ps1               # Development tasks (Windows PowerShell)
├── pyproject.toml             # Project configuration
├── README.md                  # This file
├── .gitignore                 # Git ignore file
└── output/                    # Default output directory (created after first run)
```

## Configuration

You can customize the parsing behavior by modifying the options in the Python scripts:

- Enable/disable OCR
- Configure table structure detection
- Set parsing pipelines
- Adjust performance options

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes following our [commit message guidelines](docs/contributing.md)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Docling](https://github.com/docling-project/docling) - The document parsing library
- [IBM Research](https://research.ibm.com/) - Creators of Docling
