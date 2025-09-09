# uvenv Documentation

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
uvenv python-install 3.11
```

### 2. Create a virtual environment

```bash
uvenv create myproject 3.11
```

### 3. Activate the environment

```bash
# Get activation command
uvenv activate myproject

# For bash/zsh
source ~/.uvenv/myproject/bin/activate

# Or use eval
eval "$(uvenv activate myproject)"
```

### 4. List environments

```bash
uvenv list
```

### 5. Create a lockfile

```bash
uvenv lock myproject
```

### 6. Remove an environment

```bash
uvenv remove myproject
```

## Commands

### `uvenv python-install <version>`

Install a Python version using uv.

**Arguments:**

- `version`: Python version to install (e.g., "3.11", "3.11.5")

**Example:**

```bash
uvenv python-install 3.11.0
```

### `uvenv create <name> <python_version>`

Create a new virtual environment.

**Arguments:**

- `name`: Name of the virtual environment
- `python_version`: Python version for the environment

**Example:**

```bash
uvenv create myproject 3.11
```

### `uvenv activate <name>`

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

### `uvenv list`

List all virtual environments.

**Example:**

```bash
uvenv list
```

### `uvenv remove <name>`

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

### `uvenv lock <name>`

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

### `uvenv thaw <name>`

Rebuild environment from lockfile.

**Arguments:**

- `name`: Name of the virtual environment

**Example:**

```bash
uvenv thaw myproject
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
