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

from androidMemoryTool import AndroidMemoryTool, PIDException
from utils.pprints import PPrints
from asyncio import sleep
import subprocess
import sys
import os


class RootUtils(object):
    """
    A utility class for handling root-related tasks and interacting with Android applications.
    This class provides methods for checking if a game is running, acquiring root privileges,
    and removing files.
    Attributes:
        _pprints (PPrints): An instance of the PPrints class for pretty-printing messages.
    Methods:
        is_game_running(package_name: str) -> bool:
            Check if an Android game with the specified package name is currently running.
            Args:
                package_name (str): The package name of the Android game.
            Returns:
                bool: True if the game is running; False otherwise.
        is_rooted_acquired():
            Check if the script has acquired root privileges, and if not, attempt to acquire them.
            If root privileges are not acquired, the script will be rebooted as root.
        remove_file(file_path: str):
            Remove a file at the specified path if it exists.
            Args:
                file_path (str): The path to the file to be removed.
    Note:
        This class assumes that the script is run on a system where root privileges can be acquired using 'sudo'.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initialize a RootUtils instance.
        Args:
            **kwargs: Additional keyword arguments for future extensions.
        """

        super().__init__(**kwargs)
        self._pprints = PPrints()

    @staticmethod
    async def is_game_running(package_name: str) -> bool:
        """
        Check if an Android game with the specified package name is currently running.
        Args:
            package_name (str): The package name of the Android game.
        Returns:
            bool: True if the game is running; False otherwise.
        """

        try:
            pid = AndroidMemoryTool(PKG=package_name).get_pid()
        except PIDException:
            return False

        if not pid:
            return False
        return True

    async def is_rooted_acquired(self) -> None:
        """
        Check if the script has acquired root privileges, and if not, attempt to acquire them.
        If root privileges are not acquired, the script will be rebooted as root.
        """

        if os.getuid() != 0:
            await self._pprints.pprints(text="Root Required", info_type=2)
            await self._pprints.pprints(text="Rebooting script as root", info_type=4)
            await sleep(2)
            subprocess.call(['sudo', 'python3', *sys.argv])
            sys.exit(1)
        else:
            await self._pprints.pprints(text="Root Acquired")

    @staticmethod
    async def remove_file(file_path: str) -> None:
        """
        Remove a file at the specified path if it exists.
        Args:
            file_path (str): The path to the file to be removed.
        """
        try:
            os.remove(path=file_path)
        except FileNotFoundError:
            pass
