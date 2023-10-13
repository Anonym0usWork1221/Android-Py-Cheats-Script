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

from art import tprint
import subprocess


class Colors:
    """
    This class defines various ANSI color codes for text formatting in the terminal.
    """

    C_HEADER = '\033[95m'
    C_BLUE = '\033[94m'
    C_CYAN = '\033[96m'
    C_GREEN = '\033[92m'
    C_WARNING = '\033[93m'
    C_FAIL = '\033[91m'
    C_BOLD = '\033[1m'
    C_RESET = '\033[0m'


class PPrints(object):
    """
    PPrints is a utility class for pretty-printing colored text messages in the terminal.

    Attributes:
    _INFO_TAGS (dict): A dictionary that maps information types to their corresponding tags.
    _INFO_COLORS (dict): A dictionary that maps information types to their corresponding text colors.
    _RESET_COLOR (str): The ANSI color code to reset text color to default.

    Methods:
    __init__(self, **kwargs): Constructor method for PPrints class.
    decoration(self): Display a decorative header with the project name and author information.
    pprints(self, text: str, reset_text: bool = False, info_type: int = 1, no_end: bool = False, off_info: bool = False):
        Pretty print a text message with optional formatting options.
        Args:
        text (str): The message to be printed.
        reset_text (bool): If True, clears the screen and prints the message with the decorative header.
        info_type (int): The type of information (1 for INFO, 2 for WARNING, 3 for ERROR, 4 for NEED ATTENTION).
        no_end (bool): If True, the message will not end with a newline character.
        off_info (bool): If True, the info type tag is omitted from the printed message.
    """

    _INFO_TAGS = {
        1: "[INFO]",
        2: "[WARNING]",
        3: "[ERROR]",
        4: "[NEED ATTENTION]",
    }

    _INFO_COLORS = {
        1: Colors.C_GREEN,
        2: Colors.C_WARNING,
        3: Colors.C_FAIL,
        4: Colors.C_BLUE
    }

    _RESET_COLOR = Colors.C_RESET

    def __init__(self, **kwargs) -> None:
        """
        Constructor method for PPrints class.
        Args:
        **kwargs: Additional keyword arguments (not used in this implementation).
        """

        super().__init__(**kwargs)

    async def decoration(self) -> None:
        """
        Display a decorative header with the project name and author information.
        """

        subprocess.call("clear")
        print(Colors.C_HEADER)
        tprint(text="PyCheats")
        print(f"{Colors.C_CYAN}{Colors.C_BOLD}\nBy github.com/Anonym0usWork1221\n{self._RESET_COLOR}")

    async def pprints(self, text: str, reset_text: bool = False, info_type: int = 1, no_end: bool = False,
                      off_info: bool = False) -> None:
        """
        Pretty print a text message with optional formatting options.

        Args:
            text (str): The message to be printed.
            reset_text (bool): If True, clears the screen and prints the message with the decorative header.
            info_type (int): The type of information (1 for INFO, 2 for WARNING, 3 for ERROR, 4 for NEED ATTENTION).
            no_end (bool): If True, the message will not end with a newline character.
            off_info (bool): If True, the info type tag is omitted from the printed message.
        """

        info_tag = self._INFO_TAGS.get(info_type, "[UNK]")
        info_color = self._INFO_COLORS.get(info_type, Colors.C_CYAN)
        if not off_info:
            text_assembled = f"{info_color}{info_tag}-> {text}{self._RESET_COLOR}"
        else:
            text_assembled = f"{info_color}{text}{self._RESET_COLOR}"
        if reset_text:
            await self.decoration()
            print(text_assembled)
        elif no_end:
            print(text_assembled, end="")
        else:
            print(text_assembled)

