# uvenv Design Conversation

## User's Setup

-   Works in Python a lot.
-   Uses pip for package management.
-   Uses pyenv for Python version management.
-   Uses pyenv-virtualenv for virtual environment management (stored in
    \$HOME/.pyenv/).

## Motivation

-   Started using `uv` for package management (faster).
-   Likes `uv python install <version>` and `uv venv <name>`.
-   But `uv` has no pyenv-virtualenv replacement.
-   Wants to build `uvenv` (uv-virtualenv wrapper).

## Proposed Features (User)

-   `uvenv python install <version>` (wraps uv).
-   `uvenv <venvname> <pythonversion>` to create envs stored in
    \$HOME/.uvenv/.
-   `uvenv <name> activate` to activate env.
-   `uvenv freeze` and `uvenv thaw`.
-   Autocomplete support.
-   Distribution via brew.

## Assistant: Repository Structure

    uvenv/
    ├── src/uvenv/
    │   ├── cli.py
    │   ├── core/
    │   │   ├── manager.py
    │   │   ├── python.py
    │   │   ├── paths.py
    │   │   ├── freeze.py
    │   │   └── utils.py
    │   └── shell/
    │       ├── activate.py
    │       └── completion.py
    ├── tests/
    ├── docs/
    ├── pyproject.toml
    ├── README.md
    └── .github/workflows/ci.yml

-   CLI framework: Typer (Click-based).
-   Testing: pytest.
-   Packaging: pyproject.toml, console_scripts.

## Command Design (First Iteration)

-   `uvenv python install 3.11.9`
-   `uvenv create myproj 3.11.9`
-   `uvenv activate myproj`
-   `uvenv pip install requests`
-   `uvenv freeze`

## Growth Path

-   MVP: wrap uv python + uv venv.
-   Phase 2: freeze/thaw, completions, metadata.
-   Phase 3: brew formula, global hooks, workspace isolation.

## Lockfile Design (uvenv.lock)

-   Per-env lockfile in TOML or JSON.

### Example TOML

``` toml
[env]
name = "myproj"
python = "3.11.9"
created = "2025-09-09T12:00:00Z"

[dependencies]
requests = "==2.32.3"
numpy = "==2.0.1"

[metadata]
uvenv_version = "0.1.0"
hash = "sha256:deadbeef123..."
```

-   Commands: `uvenv lock`, `uvenv thaw`, `uvenv check`, `uvenv sync`.

## Metadata File (uvenv.meta.json)

Internal details, per-env, not portable.

### Example

``` json
{
  "name": "myproj",
  "python": {
    "version": "3.11.9",
    "path": "/Users/alice/.uv/python/3.11.9/bin/python"
  },
  "paths": {
    "root": "/Users/alice/.uvenv/myproj",
    "bin": "/Users/alice/.uvenv/myproj/bin",
    "site_packages": "/Users/alice/.uvenv/myproj/lib/python3.11/site-packages"
  },
  "activation": {
    "shim_created": true,
    "shells": ["bash", "zsh"]
  },
  "uvenv_version": "0.1.0",
  "created": "2025-09-09T12:00:00Z",
  "last_used": "2025-09-09T13:15:42Z"
}
```

------------------------------------------------------------------------
