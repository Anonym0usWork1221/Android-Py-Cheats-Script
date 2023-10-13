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

from utils.requirements_intaller import ReqInstaller

ReqInstaller().install_requirements()  # Install requirements

# Required Libraries
from androidMemoryTool import AndroidMemoryTool, DataTypes, PMAP
from utils.gather_information import GameInformationHandler
from utils.root_utilities import RootUtils
from utils.pprints import PPrints
import asyncio
import sys


class PyCheats(object):
    """PyCheats - A Python-based Android game cheating tool."""

    def __init__(self, **kwargs) -> None:
        """
        Initialize the PyCheats object.

        Args:
            **kwargs: Additional keyword arguments.
        """

        super().__init__(**kwargs)
        self._game_info_handler: GameInformationHandler = GameInformationHandler()
        self._event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self._root_utils: RootUtils = RootUtils()
        self._pprints: PPrints = PPrints()

        # Memory Tools Instances Required
        # CODE APP Range instances
        self._dword_code_app_instance = None
        self._utf_8_code_app_instance = None
        self._float_code_app_instance = None

        # C_ALLOC Range Instances
        self._dword_c_alloc_instance = None
        self._float_c_alloc_instance = None

        # A_ANONYMOUS Range Instances
        self._float_a_anonymous_instance = None
        self._dword_a_anonymous_instance = None

        # C_Data Range Instances
        self._float_c_data_instance = None
        self._dword_c_data_instance = None

    async def __async__get_ticks(self) -> None:
        """
        Asynchronously get information about the Android game and initialize instances.
        This method retrieves game information, checks if the game is running, and initializes memory tool instances.
        Raises:
            SystemExit: Exits the application if the game is not running.
        """

        await self._pprints.decoration()  # Prints the PyCheat on screen
        await self._root_utils.is_rooted_acquired()  # Get root access if the device is rooted
        package_name = await self._game_info_handler.upack_information()
        if not await self._root_utils.is_game_running(package_name=package_name):
            await self._pprints.pprints(text="Game is not running", info_type=3)
            sys.exit(1)

        await self._initialize_instances(package_name=package_name)
        await self.controller_menu()

    async def _initialize_instances(self, package_name: str) -> None:
        """
        Initialize memory tool instances for various memory ranges and data types.
        Args:
            package_name (str): The package name of the Android game.
        This method initializes memory tool instances for different memory ranges and data types.
        """

        # CODE APP Range instances
        self._dword_code_app_instance = AndroidMemoryTool(PKG=package_name, pMAP=PMAP(ALL=False, CODE_APP=True),
                                                          SPEED_MODE=True, WORKERS=AndroidMemoryTool.get_cpu_counts(3))
        self._utf_8_code_app_instance = AndroidMemoryTool(PKG=package_name, pMAP=PMAP(ALL=False, CODE_APP=True),
                                                          TYPE=DataTypes.UTF_8,
                                                          SPEED_MODE=True, WORKERS=AndroidMemoryTool.get_cpu_counts(3))
        self._float_code_app_instance = AndroidMemoryTool(PKG=package_name, pMAP=PMAP(ALL=False, CODE_APP=True),
                                                          TYPE=DataTypes.FLOAT,
                                                          SPEED_MODE=True, WORKERS=AndroidMemoryTool.get_cpu_counts(3))

        # C_ALLOC Range Instances
        self._dword_c_alloc_instance = AndroidMemoryTool(PKG=package_name, pMAP=PMAP(ALL=False, C_ALLOC=True),
                                                         SPEED_MODE=True, WORKERS=AndroidMemoryTool.get_cpu_counts(3))
        self._float_c_alloc_instance = AndroidMemoryTool(PKG=package_name, pMAP=PMAP(ALL=False, C_ALLOC=True),
                                                         TYPE=DataTypes.FLOAT,
                                                         SPEED_MODE=True, WORKERS=AndroidMemoryTool.get_cpu_counts(3))

        # A_ANONYMOUS Range Instances
        self._dword_a_anonymous_instance = AndroidMemoryTool(PKG=package_name, pMAP=PMAP(ALL=False, A_ANONYMOUS=True),
                                                             SPEED_MODE=True,
                                                             WORKERS=AndroidMemoryTool.get_cpu_counts(3))
        self._float_a_anonymous_instance = AndroidMemoryTool(PKG=package_name, pMAP=PMAP(ALL=False, A_ANONYMOUS=True),
                                                             TYPE=DataTypes.FLOAT, SPEED_MODE=True,
                                                             WORKERS=AndroidMemoryTool.get_cpu_counts(3))

        # C_Data Range Instances
        self._dword_c_data_instance = AndroidMemoryTool(PKG=package_name, pMAP=PMAP(ALL=False, C_DATA=True),
                                                        SPEED_MODE=True, WORKERS=AndroidMemoryTool.get_cpu_counts(3))
        self._float_c_data_instance = AndroidMemoryTool(PKG=package_name, pMAP=PMAP(ALL=False, C_DATA=True),
                                                        TYPE=DataTypes.FLOAT,
                                                        SPEED_MODE=True, WORKERS=AndroidMemoryTool.get_cpu_counts(3))

    async def logo_bypass(self) -> None:
        """
        Perform a logo bypass to modify game values.
        This method modifies various game values to bypass the game's anti-cheat system.
        """

        utf_8_anti_cheat = ["libUE4.so", "libBugly.so", "libanogs.so", "l_report", "get_report",
                            "tss_sdk_rcv_anti_data", "AreaData.dat", "AntiCheatData", "Reports", "hack", "ban",
                            "cheat", "qq.com"
                            ]
        code_app_dword_values = [118334, 856896, 123010, 123179, 123274, 1026]
        code_app_float_values = [9.21970312e-41, 13073.3740234375]
        offsets_libUE4_dword = ['0x7E2A78', '0x7E2A80', '0x7E2A88']

        replaced_value: int = 0
        for value in utf_8_anti_cheat:
            replaced_value += self._utf_8_code_app_instance.read_write_value(read=value, write="ruler_king")

        for value in code_app_dword_values:
            replaced_value += self._dword_code_app_instance.read_write_value(read=value, write=1)

        for value in code_app_float_values:
            replaced_value += self._float_code_app_instance.read_write_value(read=value, write=0.1)

        lib_offset = self._dword_code_app_instance.get_module_base_address("libUE4.so")
        for value in offsets_libUE4_dword:
            if self._dword_code_app_instance.write_lib(base_address=lib_offset, offset=value,
                                                       write_value=1):
                replaced_value += 1

        await self._pprints.pprints(text=f"Updated {replaced_value} Values")

    @staticmethod
    async def write_group_values_with_filter(instance, read: list, write: any, refine: any = None,
                                             limit: int = -1) -> int:
        """
        Write values to memory based on specified filter criteria.
        Args:
            instance: An instance of the memory tool.
            read (list): A list of values to read from memory.
            write: The value to write to memory.
            refine: A value to refine memory addresses (optional).
            limit: The maximum number of values to modify (optional).
        Returns:
            int: The number of values replaced.
        This method writes values to memory based on the specified criteria.
        """

        value_replaced: int = 0
        group_values = instance.read_value(read=read, is_grouped=True)
        if group_values:
            if refine:
                group_values = instance.refiner_address(list_address=group_values[0], value_to_refine=refine)
            if limit > 0:
                group_values = group_values[:limit]
            for value in group_values:
                if instance.write_lib(base_address=value, offset='0x0', write_value=write):
                    value_replaced += 1

        return value_replaced

    async def lobby_bypass(self) -> None:
        """
        Perform a lobby bypass to remove unnecessary files and modify game values.
        This method removes unnecessary files and modifies game values to bypass the game's
        anti-cheat system in the lobby.
        """

        unnecessary_files = [
            "src/main/java/com/google/errorprone/annotations",
            "src/main/java/com/google/errorprone/annotations/concurrent",
            "third_party.java_src.error_prone.project.annotations.Google_internal"
        ]
        refine_groups = {
            self._dword_c_alloc_instance: [
                {"value": [135682, 144387], "replace": 67109633, "refine": 135682, "limit": 50000},
                {"value": [134914, 262403], "replace": 67109633, "refine": 134914, "limit": 50000},
                {"value": [134658, 131586], "replace": 67109633, "refine": 134658, "limit": 50000},
                {"value": [133378, 262403], "replace": 67109633, "refine": 133378, "limit": 50000},
                {"value": [131842, 132098], "replace": 67109633, "refine": 131842, "limit": 50000},
            ]
        }
        # Removing some unnecessary files
        values_replaced: int = 0
        for file in unnecessary_files:
            await self._root_utils.remove_file(file_path=file)

        for key, values in refine_groups.items():
            for value in values:
                values_replaced += await self.write_group_values_with_filter(
                    instance=key,
                    read=value["value"],
                    refine=value["refine"],
                    limit=value["limit"],
                    write=value["replace"]
                )

    async def basic_cheats(self, cheat_code: int) -> None:
        """
        Activate basic game cheats based on the specified cheat code.
        Args:
            cheat_code (int): The code for the desired cheat.
        This method activates basic game cheats such as HEADSHOT, ANTENNA, AIM-BOT, and SPEED-HACK.
        """

        basic_cheat_sheet = {
            1: "HEADSHOT",
            2: "ANTENNA",
            3: "AIM-BOT",
            4: "SPEED-HACK"
        }
        cheat = basic_cheat_sheet.get(cheat_code, None)
        match cheat:
            case "HEADSHOT":
                address_list = []
                address_list.extend(self._float_a_anonymous_instance.read_value(read=[9.20161819458, 23.0, 25.0, 30.5],
                                                                                is_grouped=True)[0])

                address_list.extend(self._float_a_anonymous_instance.read_value(read=[25.0, 30.5], is_grouped=True)[0])
                address_list = address_list[:10]  # Get only 10 results
                for address in address_list:
                    self._float_a_anonymous_instance.write_lib(base_address=address, offset='0x0', write_value=240.0)

                await self._pprints.pprints(text=f"Activated Headshot Cheat")

            case "ANTENNA":
                address_list = []
                address_list.extend(self._float_a_anonymous_instance.read_value(read=[88.50576019287,
                                                                                      87.27782440186, 1],
                                                                                is_grouped=True, range_val=13)[0])

                address_list.extend(self._float_a_anonymous_instance.read_value(read=[25.0, 30.5], is_grouped=True)[0])
                address_list = address_list[:6]  # Get only 6 results
                for address in address_list:
                    self._float_a_anonymous_instance.write_lib(base_address=address, offset='0x0', write_value=1.96875)

                await self._pprints.pprints(text=f"Activated ANTENNA Cheat")

            case "AIM-BOT":
                address_list = []
                address_list.extend(self._float_a_anonymous_instance.read_value(read=[360.0, 0.0001, 1478828288.0],
                                                                                is_grouped=True)[0])

                address_list.extend(self._float_a_anonymous_instance.read_value(read=0.0001, is_grouped=False)[0])
                address_list = address_list[:100]  # Get only 100 results
                for address in address_list:
                    self._float_a_anonymous_instance.write_lib(base_address=address, offset='0x0', write_value=9999.0)

                await self._pprints.pprints(text=f"Activated AIM-BOT Cheat")

            case "SPEED-HACK":
                address_list = []
                address_list.extend(self._float_a_anonymous_instance.read_value(read=[1.0, 1.0, 1.0, 0.0001, 20.0,
                                                                                      0.0005, 0.4],
                                                                                is_grouped=True, range_val=50)[0])

                address_list.extend(self._float_a_anonymous_instance.read_value(read=1, is_grouped=False)[0])
                address_list = address_list[:100]  # Get only 100 results
                for address in address_list:
                    self._float_a_anonymous_instance.write_lib(base_address=address, offset='0x0', write_value=1.5)

                address_list.clear()
                address_list.extend(self._float_c_data_instance.read_value(read=[-6.1526231e27, -1.0070975e28],
                                                                           is_grouped=True)[0])

                address_list.extend(self._float_c_data_instance.read_value(read=-6.1526231e27, is_grouped=False)[0])
                address_list = address_list[:1]  # Get only 100 results
                for address in address_list:
                    self._float_a_anonymous_instance.write_lib(base_address=address, offset='0x0', write_value=0.01)

                await self._pprints.pprints(text=f"Activated SPEED-HACK Cheat")

    async def controller_menu(self) -> None:
        """
        Display a controller menu to interact with the PyCheats tool.
        This method displays a menu with options for performing various actions using the PyCheats tool.
        """

        while True:
            await self._pprints.pprints(text="1. Logo Anti-Cheat System", off_info=True)
            await self._pprints.pprints(text="2. Lobby Anti-Cheat System", off_info=True)
            await self._pprints.pprints(text="3. HEADSHOT", off_info=True)
            await self._pprints.pprints(text="4. ANTENNA", off_info=True)
            await self._pprints.pprints(text="5. AIM-BOT", off_info=True)
            await self._pprints.pprints(text="6. SPEED-HACK", off_info=True)
            await self._pprints.pprints(text="7. Dump Maps", off_info=True)
            await self._pprints.pprints(text="8. Exit", off_info=True)
            await self._pprints.pprints(text=">>>> ", off_info=True, info_type=5, no_end=True)
            ans = input()
            ans = int(ans)
            match ans:
                case 1:
                    await self.logo_bypass()
                case 2:
                    await self.lobby_bypass()
                case 3:
                    await self.basic_cheats(cheat_code=1)
                case 4:
                    await self.basic_cheats(cheat_code=2)
                case 5:
                    await self.basic_cheats(cheat_code=3)
                case 6:
                    await self.basic_cheats(cheat_code=4)
                case 7:
                    self._float_c_data_instance.dump_maps()
                case 8:
                    sys.exit(0)
                case _:
                    await self._pprints.pprints(text="Choose given options", info_type=2)
                    await asyncio.sleep(2)

    def get_ticks(self) -> None:
        """
        Start the PyCheats tool and enter the event loop to interact with the controller menu.
        """

        self._event_loop.run_until_complete(self.__async__get_ticks())


if __name__ == '__main__':
    py_cheats_object = PyCheats()
    py_cheats_object.get_ticks()
