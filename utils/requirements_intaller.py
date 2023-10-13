"""
/*
 *  Date     : 2023/10/13
 *  Version  : 0.3
 *  Author   : Abdul Moez
 *  Email    : abdulmoez123456789@gmail.com
 *  Affiliation : Undergraduate at Government College University (GCU) Lahore, Pakistan
 *  GitHub   : https://github.com/Anonym0usWork1221/android-memorytool
 *
 */
"""

import os


class ReqInstaller(object):
    """
    ReqInstaller is a class for managing the installation of required dependencies for a Python script.
    Usage:
    - Create an instance of ReqInstaller.
    - Call the install_requirements method to ensure the required packages are installed.
    Attributes:
    None
    Methods:
    - install_requirements(): Installs required Python packages.
                              If run as a superuser, it attempts to install packages globally.
    - _is_rooted_acquired(): Checks if the script is running with superuser privileges.
    Note:
    To use this class, you must have the 'androidMemoryTool' and 'art' Python packages available or installable.
    """

    def __init__(self) -> None:
        """
        Initialize a new instance of ReqInstaller.
        Args:
            None
        Returns:
            None
        """
        ...

    @staticmethod
    def _is_rooted_acquired() -> bool:
        """
        Check if the script is running with superuser (root) privileges.
        Args:
            None
        Returns:
            bool: True if running with superuser privileges, False otherwise.
        """

        if os.getuid() != 0:
            return False
        return True

    def install_requirements(self) -> None:
        """
        Install required Python packages based on script's import availability and superuser status.
        Args:
            None
        Returns:
            None
        Notes:
            - If 'androidMemoryTool' and 'art' are importable, no action is taken.
            - If not importable and the script is run with superuser privileges, it attempts to
              install the packages globally.
            - If not importable and the script is not run as superuser, it installs required packages locally.
        """

        try:
            from androidMemoryTool import AndroidMemoryTool
            from art import tprint
        except ImportError:
            import subprocess
            import sys
            if self._is_rooted_acquired():
                # Run Script without root to install requirements
                subprocess.call(['python3', *sys.argv])
                sys.exit(0)
            else:
                print("[+] Installing requirements")
                os.system("pip3 install -r ./requirements.txt")
                subprocess.call(['sudo', 'python3', *sys.argv])
                sys.exit(0)

