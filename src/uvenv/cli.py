"""CLI entrypoint for uvenv using Typer."""

import typer
from rich.console import Console
from rich.table import Table

from uvenv import __version__
from uvenv.core.freeze import FreezeManager
from uvenv.core.manager import EnvironmentManager
from uvenv.core.python import PythonManager

console = Console()


def version_callback(value: bool) -> None:
    """Handle version option."""
    if value:
        console.print(f"uvenv version {__version__}")
        raise typer.Exit()


app = typer.Typer(
    name="uvenv",
    help="A CLI tool for managing Python virtual environments using uv",
    rich_markup_mode="rich",
)


@app.callback()
def main_callback(
    _version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """Main callback for global options."""


# Initialize managers
env_manager = EnvironmentManager()
python_manager = PythonManager()
freeze_manager = FreezeManager()


@app.command()
def python_install(
    version: str = typer.Argument(..., help="Python version to install"),
) -> None:
    """Install a Python version using uv."""
    console.print(f"[green]Installing Python {version}...[/green]")
    try:
        python_manager.install(version)
        console.print(f"[green]✓[/green] Python {version} installed successfully")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to install Python {version}: {e}")
        raise typer.Exit(1) from None


@app.command()
def create(
    name: str = typer.Argument(..., help="Name of the virtual environment"),
    python_version: str = typer.Argument(
        ..., help="Python version for the environment"
    ),
) -> None:
    """Create a new virtual environment."""
    console.print(
        f"[green]Creating environment '{name}' with Python {python_version}...[/green]"
    )
    try:
        env_manager.create(name, python_version)
        console.print(f"[green]✓[/green] Environment '{name}' created successfully")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to create environment '{name}': {e}")
        raise typer.Exit(1) from None


@app.command()
def activate(
    name: str = typer.Argument(..., help="Name of the virtual environment"),
) -> None:
    """Print shell activation snippet for the environment."""
    try:
        activation_script = env_manager.get_activation_script(name)
        console.print(activation_script)
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to get activation script for '{name}': {e}")
        raise typer.Exit(1) from None


@app.command()
def list() -> None:
    """List all virtual environments."""
    try:
        environments = env_manager.list()
        if not environments:
            console.print("[yellow]No virtual environments found[/yellow]")
            return

        table = Table(title="Virtual Environments")
        table.add_column("Name", style="cyan")
        table.add_column("Python Version", style="green")
        table.add_column("Path", style="blue")
        table.add_column("Status", style="magenta")

        for env in environments:
            table.add_row(
                env["name"], env["python_version"], env["path"], env["status"]
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to list environments: {e}")
        raise typer.Exit(1) from None


@app.command()
def remove(
    name: str = typer.Argument(..., help="Name of the virtual environment"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force removal without confirmation"
    ),
) -> None:
    """Remove a virtual environment."""
    if not force:
        confirm = typer.confirm(
            f"Are you sure you want to remove environment '{name}'?"
        )
        if not confirm:
            console.print("[yellow]Operation cancelled[/yellow]")
            return

    try:
        env_manager.remove(name)
        console.print(f"[green]✓[/green] Environment '{name}' removed successfully")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to remove environment '{name}': {e}")
        raise typer.Exit(1) from None


@app.command()
def lock(
    name: str = typer.Argument(..., help="Name of the virtual environment"),
) -> None:
    """Generate a lockfile for the environment."""
    console.print(f"[green]Generating lockfile for environment '{name}'...[/green]")
    try:
        freeze_manager.lock(name)
        console.print(f"[green]✓[/green] Lockfile generated for '{name}'")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to generate lockfile for '{name}': {e}")
        raise typer.Exit(1) from None


@app.command()
def thaw(
    name: str = typer.Argument(..., help="Name of the virtual environment"),
) -> None:
    """Rebuild environment from lockfile."""
    console.print(f"[green]Rebuilding environment '{name}' from lockfile...[/green]")
    try:
        freeze_manager.thaw(name)
        console.print(f"[green]✓[/green] Environment '{name}' rebuilt from lockfile")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to rebuild environment '{name}': {e}")
        raise typer.Exit(1) from None


if __name__ == "__main__":
    app()
