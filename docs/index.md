# uvenv Documentation

## 📚 Documentation Navigation

- **[User Guide](index.md)** - Complete usage documentation (this page)
- **[Design Principles](principles.md)** - Core principles and architecture decisions
- **[Roadmap](roadmap.md)** - Future development plans and phases
- **[Design Document](design.md)** - Technical implementation details

## Overview

`uvenv` is a CLI tool for managing Python virtual environments using [uv](https://github.com/astral-sh/uv). It provides a simple interface similar to `pyenv-virtualenv` but leverages the speed and efficiency of `uv`.

## Installation

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) installed and available in PATH

### Install uvenv

```bash
pip install uvenv
```

## Quick Start

### 1. Install a Python version

```bash
uvenv python install 3.11
```

### 2. List available Python versions

```bash
uvenv python list
```

### 3. Create a virtual environment

```bash
uvenv create myproject 3.11
```

### 4. Activate the environment

```bash
# Get activation command
uvenv activate myproject

# For bash/zsh
source ~/.uvenv/myproject/bin/activate

# Or use eval
eval "$(uvenv activate myproject)"
```

### 5. List environments

```bash
uvenv list
```

### 6. Create a lockfile

```bash
uvenv lock myproject
```

### 7. Remove an environment

```bash
uvenv remove myproject
```

## Commands

### Python Version Management

#### `uvenv python install <version>`

Install a Python version using uv.

**Arguments:**

- `version`: Python version to install (e.g., "3.11", "3.11.5")

**Example:**

```bash
uvenv python install 3.11.0
```

#### `uvenv python list`

List available and installed Python versions.

**Example:**

```bash
uvenv python list
```

**Output:**

- Shows a table with version names, installation status, and locations
- ✓ Installed versions are marked with a checkmark
- Available versions show as "Available"

#### `uvenv python --help`

Show help for Python version management commands.

**Example:**

```bash
uvenv python --help
```

### Environment Management

#### `uvenv create <name> <python_version>`

Create a new virtual environment.

**Arguments:**

- `name`: Name of the virtual environment
- `python_version`: Python version for the environment

**Example:**

```bash
uvenv create myproject 3.11
```

#### `uvenv activate <name>`

Print shell activation snippet for the environment.

**Arguments:**

- `name`: Name of the virtual environment

**Example:**

```bash
# Print activation command
uvenv activate myproject

# Use with eval
eval "$(uvenv activate myproject)"
```

#### `uvenv list`

List all virtual environments.

**Example:**

```bash
uvenv list
```

#### `uvenv remove <name>`

Remove a virtual environment.

**Arguments:**

- `name`: Name of the virtual environment

**Options:**

- `--force`, `-f`: Force removal without confirmation

**Example:**

```bash
uvenv remove myproject
uvenv remove myproject --force
```

### Lockfile Management

#### `uvenv lock <name>`

Generate a lockfile for the environment.

**Arguments:**

- `name`: Name of the virtual environment

**Example:**

```bash
uvenv lock myproject
```

This creates a `uvenv.lock` file in the environment directory containing:

- Environment name and Python version
- List of installed packages with exact versions
- Platform information
- Generation timestamp

#### `uvenv thaw <name>`

Rebuild environment from lockfile.

**Arguments:**

- `name`: Name of the virtual environment

**Example:**

```bash
uvenv thaw myproject
```

## Python Version Workflow Examples

### Installing and Managing Python Versions

```bash
# Check what Python versions are available
uvenv python list

# Install a specific Python version
uvenv python install 3.12.1

# Install multiple versions for different projects
uvenv python install 3.11.7
uvenv python install 3.10.13

# List all versions again to see installed ones
uvenv python list
```

### Complete Project Setup Workflow

```bash
# 1. Install the Python version you need
uvenv python install 3.12.1

# 2. Create a virtual environment for your project
uvenv create myproject 3.12.1

# 3. Activate the environment
eval "$(uvenv activate myproject)"

# 4. Install packages in your activated environment
pip install requests fastapi

# 5. Create a lockfile to save the exact environment state
uvenv lock myproject

# 6. Later, recreate the environment from the lockfile
uvenv thaw myproject
```

### Managing Multiple Projects

```bash
# Set up environments for different projects
uvenv python install 3.11.7
uvenv python install 3.12.1

uvenv create api-project 3.12.1
uvenv create legacy-project 3.11.7

# See all your environments
uvenv list

# Switch between projects
eval "$(uvenv activate api-project)"
# ... work on api project

eval "$(uvenv activate legacy-project)"
# ... work on legacy project
```

## Configuration

### Environment Storage

By default, virtual environments are stored in `~/.uvenv/`. Each environment is stored in its own directory:

```
~/.uvenv/
├── myproject/
│   ├── bin/activate           # Activation script
│   ├── lib/python3.11/        # Python packages
│   ├── uvenv.lock            # Lockfile
│   └── uvenv.meta.json       # Metadata
└── another-env/
    ├── bin/activate
    ├── lib/python3.10/
    ├── uvenv.lock
    └── uvenv.meta.json
```

### Lockfile Format

The `uvenv.lock` file is in TOML format:

```toml
[uvenv]
version = "0.1.0"
generated = "2023-12-01T12:00:00"

[environment]
name = "myproject"
python_version = "3.11.0"

dependencies = [
    "requests==2.31.0",
    "click==8.1.7",
    # ... other packages
]

[metadata]
locked_at = "2023-12-01T12:00:00"

[metadata.platform]
system = "Darwin"
machine = "arm64"
python_implementation = "CPython"
```

## Shell Integration

### Bash/Zsh

Add to your `.bashrc` or `.zshrc`:

```bash
# Function to activate uvenv environments
uvactivate() {
    if [ -z "$1" ]; then
        echo "Usage: uvactivate <environment_name>"
        return 1
    fi
    eval "$(uvenv activate "$1")"
}
```

### Fish

Add to your Fish config:

```fish
# Function to activate uvenv environments
function uvactivate
    if test (count $argv) -eq 0
        echo "Usage: uvactivate <environment_name>"
        return 1
    end
    eval (uvenv activate $argv[1])
end
```

## Best Practices

1. **Use lockfiles**: Always create lockfiles for reproducible environments
2. **Meaningful names**: Use descriptive environment names
3. **Clean up**: Remove unused environments regularly
4. **Version pinning**: Use specific Python versions for consistency

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/mgale694/uvenv.git
cd uvenv

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Quality

uvenv uses modern Python tooling for code quality:

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/ --fix

# Type checking
mypy src/

# Run tests
pytest tests/

# Run pre-commit on all files
pre-commit run --all-files
```

### Pre-commit Hooks

The project includes pre-commit hooks for:

- Code formatting (black)
- Linting (ruff)
- Type checking (mypy)
- Standard checks (trailing whitespace, YAML/TOML validation)

## Troubleshooting

### Common Issues

**uv not found:**

```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Permission errors:**

```bash
# Ensure ~/.uvenv is writable
chmod 755 ~/.uvenv
```

**Environment not activating:**

```bash
# Check if environment exists
uvenv list

# Recreate if necessary
uvenv remove myproject
uvenv create myproject 3.11
```
