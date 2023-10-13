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

from utils.pprints import PPrints
from json import loads, dump
from os import path


class GameInformationHandler(object):
    """
    GameInformationHandler is a class for managing game information.
    This class allows you to compare, retrieve, and update game package information.
    It is particularly useful for managing Android game package data.
    Args:
        **kwargs: Additional keyword arguments for customization.
    Attributes:
        _pprints (PPrints): An instance of the PPrints class for pretty printing.
    Methods:
        compare() -> bool:
            Compare the current game package name with a stored one.
        get_data() -> None:
            Prompt the user to enter a game package name and store it in a JSON file.
        unpack_information() -> str:
            Retrieve the stored game package name.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._pprints = PPrints()

    async def compare(self) -> bool:
        """
        Compare the current game package name with a stored one.
        Returns:
           bool: True if the game package exists, False otherwise.
        """

        if not path.isfile("process_info.json"):
            return False

        with open("process_info.json", 'r') as json_file:
            current_info = loads(json_file.read())

        game_package_name = current_info["game_pkg"]

        if not game_package_name:
            return False

        elif path.exists(f"/storage/emulated/0/Android/data/{game_package_name}"):
            return True

        else:
            await self._pprints.pprints(text="Package not found. Please type it again or press Ctrl+C to exit.",
                                        info_type=3)
            return False

    async def get_data(self) -> None:
        """
        Prompt the user to enter a game package name and store it in a JSON file.
        """

        while not (await self.compare()):
            try:
                await self._pprints.pprints(text="Enter package name: ", info_type=4, no_end=True, off_info=True)
                pkg_name = input()
                print()
                process_info = {"game_pkg": pkg_name}
                dump(process_info, open("process_info.json", "w"))
            except KeyboardInterrupt:
                break

    async def upack_information(self) -> str:
        """
        Retrieve the stored game package name.
        Returns:
            str: The stored game package name.
        """

        await self.get_data()
        with open("process_info.json", 'r') as json_file:
            current_info = loads(json_file.read())
        game_package_name = current_info["game_pkg"]

        return game_package_name
