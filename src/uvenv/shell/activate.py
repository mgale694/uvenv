"""Shell activation script generation for uvenv."""

import os
from pathlib import Path
from typing import Optional

from uvenv.core.paths import PathManager


class ActivationManager:
    """Manages shell activation scripts for virtual environments."""

    def __init__(self, base_dir: Optional[str] = None) -> None:
        """Initialize the activation manager.

        Args:
            base_dir: Base directory for environments
        """
        self.path_manager = PathManager(base_dir)

    def get_activation_script(self, name: str, shell: Optional[str] = None) -> str:
        """Generate activation script for a given environment and shell.

        Args:
            name: Environment name
            shell: Shell type (bash, zsh, fish, etc.). Auto-detected if None

        Returns:
            Shell activation script

        Raises:
            RuntimeError: If environment doesn't exist
        """
        if not self.path_manager.environment_exists(name):
            raise RuntimeError(f"Environment '{name}' does not exist")

        if shell is None:
            shell = self._detect_shell()

        bin_path = self.path_manager.get_env_bin_path(name)

        if shell in ("bash", "zsh"):
            return self._generate_bash_script(bin_path)
        elif shell == "fish":
            return self._generate_fish_script(bin_path)
        elif shell == "powershell":
            return self._generate_powershell_script(bin_path)
        else:
            # Default to bash-compatible
            return self._generate_bash_script(bin_path)

    def get_deactivation_script(self, shell: Optional[str] = None) -> str:
        """Generate deactivation script.

        Args:
            shell: Shell type. Auto-detected if None

        Returns:
            Shell deactivation script
        """
        if shell is None:
            shell = self._detect_shell()

        if shell in ("bash", "zsh"):
            return "deactivate"
        elif shell == "fish":
            return "deactivate"
        elif shell == "powershell":
            return "deactivate"
        else:
            return "deactivate"

    def _detect_shell(self) -> str:
        """Detect the current shell.

        Returns:
            Shell name
        """
        shell_env = os.environ.get("SHELL", "")

        if "bash" in shell_env:
            return "bash"
        elif "zsh" in shell_env:
            return "zsh"
        elif "fish" in shell_env:
            return "fish"
        elif os.name == "nt":
            return "powershell"
        else:
            return "bash"  # Default

    def _generate_bash_script(self, bin_path: Path) -> str:
        """Generate bash/zsh activation script.

        Args:
            bin_path: Path to environment bin directory

        Returns:
            Bash activation script
        """
        activate_script = bin_path / "activate"
        return f"source {activate_script}"

    def _generate_fish_script(self, bin_path: Path) -> str:
        """Generate fish activation script.

        Args:
            bin_path: Path to environment bin directory

        Returns:
            Fish activation script
        """
        activate_script = bin_path / "activate.fish"
        return f"source {activate_script}"

    def _generate_powershell_script(self, bin_path: Path) -> str:
        """Generate PowerShell activation script.

        Args:
            bin_path: Path to environment Scripts directory

        Returns:
            PowerShell activation script
        """
        activate_script = bin_path / "Activate.ps1"
        return f"& {activate_script}"
