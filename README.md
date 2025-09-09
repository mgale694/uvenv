# uvenv

[![CI](https://github.com/mgale694/uvenv/workflows/CI/badge.svg)](https://github.com/mgale694/uvenv/actions)
[![PyPI version](https://badge.fury.io/py/uvenv.svg)](https://badge.fury.io/py/uvenv)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A CLI tool for managing Python virtual environments using [uv](https://github.com/astral-sh/uv). Think `pyenv-virtualenv` but powered by the speed of `uv`.

## Features

- 🚀 **Fast**: Leverages uv's speed for Python installation and environment creation
- 🎯 **Simple**: Intuitive CLI commands for common virtual environment operations
- 🔒 **Reproducible**: Lockfile support for consistent environments across systems
- 🐚 **Shell Integration**: Easy activation/deactivation in bash, zsh, fish, and PowerShell
- 📊 **Metadata**: Track environment usage and metadata

## Quick Start

### Installation

```bash
pip install uvenv
```

### Prerequisites

Ensure [uv](https://github.com/astral-sh/uv) is installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Basic Usage

```bash
# Install a Python version
uvenv python-install 3.11

# Create a virtual environment
uvenv create myproject 3.11

# Activate the environment
eval "$(uvenv activate myproject)"

# List environments
uvenv list

# Create a lockfile
uvenv lock myproject

# Remove an environment
uvenv remove myproject
```

## Commands

| Command                          | Description                             |
| -------------------------------- | --------------------------------------- |
| `uvenv python-install <version>` | Install a Python version using uv       |
| `uvenv create <name> <version>`  | Create a new virtual environment        |
| `uvenv activate <name>`          | Print shell activation snippet          |
| `uvenv list`                     | List all virtual environments           |
| `uvenv remove <name>`            | Remove a virtual environment            |
| `uvenv lock <name>`              | Generate a lockfile for the environment |
| `uvenv thaw <name>`              | Rebuild environment from lockfile       |

## Environment Storage

Virtual environments are stored in `~/.uvenv/`:

```
~/.uvenv/
├── myproject/
│   ├── bin/activate           # Activation script
│   ├── lib/python3.11/        # Python packages
│   ├── uvenv.lock            # Lockfile (TOML format)
│   └── uvenv.meta.json       # Metadata
└── another-env/
    └── ...
```

## Shell Integration

Add to your shell config for easier activation:

### Bash/Zsh

```bash
# Add to ~/.bashrc or ~/.zshrc
uvactivate() {
    if [ -z "$1" ]; then
        echo "Usage: uvactivate <environment_name>"
        return 1
    fi
    eval "$(uvenv activate "$1")"
}
```

### Fish

```fish
# Add to ~/.config/fish/config.fish
function uvactivate
    if test (count $argv) -eq 0
        echo "Usage: uvactivate <environment_name>"
        return 1
    end
    eval (uvenv activate $argv[1])
end
```

## Lockfile Format

uvenv uses TOML lockfiles for reproducible environments:

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
platform = { system = "Darwin", machine = "arm64" }
```

## Development

### Setup

```bash
git clone https://github.com/mgale694/uvenv.git
cd uvenv
uv pip install -e ".[dev]"
```

### Testing

```bash
pytest tests/
```

### Linting

```bash
ruff check src/ tests/
black src/ tests/
mypy src/
```

## Documentation

- 📖 [Complete Documentation](docs/index.md) - Comprehensive user guide
- 🏗️ [Design Principles](docs/principles.md) - Core principles and architecture
- 🗺️ [Roadmap](docs/roadmap.md) - Future plans and development phases
- 📐 [Design Document](docs/design.md) - Technical design and implementation details

## Roadmap

uvenv follows a phased development approach:

### ✅ Phase 1: MVP (Complete)

- Core environment management (`create`, `list`, `activate`, `remove`)
- Python version integration with uv
- Lockfile support (`lock`, `thaw`) with TOML format
- Cross-platform shell integration
- Rich CLI with beautiful output

### 🚀 Phase 2: Enhanced Features (In Progress)

- Advanced shell completions and auto-installation
- Rich metadata and environment templates
- Usage analytics and cleanup automation
- Environment sync and bulk operations

### 🌟 Phase 3: Ecosystem Integration (Planned)

- Homebrew formula and package manager distribution
- Global hooks with `.uvenv-version` files
- Project linking and workspace isolation
- IDE integrations (VS Code, PyCharm)

### 🔗 Phase 4: uv Ecosystem Integration (Future)

- Deep integration with uv project workflows
- Shared configuration and unified developer experience
- `uv.lock` linking and project synchronization

### 🦀 Phase 5: Rust Evolution (Consideration)

- Performance optimization with Rust rewrite
- Static binary distribution
- Ecosystem alignment with uv's technology stack

See the [full roadmap](docs/roadmap.md) for detailed timelines and features.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [uv](https://github.com/astral-sh/uv) - The fast Python package installer and resolver
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) - Inspiration for the interface
