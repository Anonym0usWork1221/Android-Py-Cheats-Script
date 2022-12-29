#! /usr/bin/env python

"""
 *  date   : 2022/12/29
 *  Version : 0.2
 *  author : Abdul Moez (abdulmoez123456789@gmail.com)
 *  Study  : UnderGraduate in GCU Lahore, Pakistan

"""

from os import getcwd
from sys import exit, argv
from subprocess import call
from GameInfo import get_data
from os import getuid
from json import loads
from asyncio import sleep, get_event_loop

try:
    from androidMemoryTool import AndroidMemoryTool
    from art import tprint

except ImportError:
    from os import system
    print("[+] Installing requirements")
    system("pip3 install -r ./requirements.txt")
    call(['sudo', 'python3', *argv])
    exit(0)


class Colors:
    C_HEADER = '\033[95m'
    C_BLUE = '\033[94m'
    C_CYAN = '\033[96m'
    C_GREEN = '\033[92m'
    C_WARNING = '\033[93m'
    C_FAIL = '\033[91m'
    C_BOLD = '\033[1m'


class PyCheats(Colors):
    _pkg = None
    _PID = None
    _libanogs_base = 0x0
    _libUE4_base = 0x0
    _is64 = None
    _lib_libanogs = None
    _MemTool_UTF8 = None
    _MemTool_DWORD = None
    _MemTool_FLOAT = None
    _SPEED_MODE = True
    _event_loop = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._event_loop = get_event_loop()

    async def __async__get_ticks(self):
        # initialization directory and decoration
        await self.decoration()
        await self.is_rooted_acquired()

        # Grabbing ids and setting up libs
        self._pkg = await self.grab_data()

        """ Checking if the game running and and getting pid """
        if await self.is_game_running():
            print(self.C_GREEN + "[+] Game is Running.\n")
        else:
            print(self.C_FAIL + "[+] Game is not running. Try restarting game.")
            exit(1)

        """Initializing Android Memory Tool for different data types and maps"""
        self._MemTool_UTF8 = AndroidMemoryTool(PKG=self._pkg, TYPE=AndroidMemoryTool.DataTypes.UTF_8,
                                               SPEED_MODE=self._SPEED_MODE, WORKERS=55,
                                               pMAP=AndroidMemoryTool.PMAP(ALL=False, CODE_APP=True, C_DATA=True))

        self._MemTool_DWORD = AndroidMemoryTool(PKG=self._pkg, TYPE=AndroidMemoryTool.DataTypes.DWORD,
                                                SPEED_MODE=self._SPEED_MODE, WORKERS=55,
                                                pMAP=AndroidMemoryTool.PMAP(ALL=False, CODE_APP=True))

        self._MemTool_FLOAT = AndroidMemoryTool(PKG=self._pkg, TYPE=AndroidMemoryTool.DataTypes.FLOAT,
                                                SPEED_MODE=self._SPEED_MODE, WORKERS=55,
                                                pMAP=AndroidMemoryTool.PMAP(ALL=False, CODE_APP=True))

        """Module Imported at runtime"""
        # self.change_lib(self.data)
        self._libanogs_base = AndroidMemoryTool.get_module_base_address(self._PID, "libanogs.so")
        self._libUE4_base = AndroidMemoryTool.get_module_base_address(self._PID, "libUE4.so")

        # calling logoBypass and getting base address
        print(self.C_GREEN + "[*] Security dispatching started")

        await self.logo_bypass_utf8()
        await self.logo_bypass_offset()
        await self.logo_bypass_dword()
        await self.logo_bypass_float()
        print(self.C_GREEN + "[*] Security dispatching Completed")

        await self.decoration()
        await self.lobby_work()

    """-------------------------------------Information Functions --------------------------------------------"""

    @staticmethod
    async def upack_information() -> str:
        with open("process_info.json", 'r') as json_file:
            current_info = loads(json_file.read())
            json_file.close()

        game_package_name = current_info["game_pkg"]

        return game_package_name

    async def is_rooted_acquired(self):
        if getuid() != 0:
            print(self.C_WARNING + "[-] Root Required")
            print(self.C_GREEN + "[+] Rebooting script as root")
            await sleep(2)
            call(['sudo', 'python3', *argv])
            exit(1)
        else:
            print(self.C_GREEN + "[+] Root Acquired")

    async def decoration(self):
        call("clear")
        print(self.C_HEADER)
        tprint(text="PyCheats", chr_ignore=True)
        print(self.C_CYAN + self.C_BOLD + "\nBy github.com/Anonym0usWork1221\n")

    async def grab_data(self) -> str:
        await get_data()
        return await self.upack_information()

    async def is_game_running(self) -> bool:
        self._PID = AndroidMemoryTool.get_pid(self._pkg)

        if not self._PID == "":
            return True
        else:
            return False

    """-------------------------------------Information Functions Ending--------------------------------------------"""
    """-------------------------------------AntiCheat Patching --------------------------------------------"""

    async def logo_bypass_utf8(self) -> None:
        vals_bytes = ["libUE4.so", "libBugly.so", "libanogs.so", "l_report", "get_report", "tss_sdk_rcv_anti_data",
                      "AreaData.dat",
                      "AntiCheatData", "Reports", "hack", "ban", "cheat", "qq.com", "tencent.com", "packets.com",
                      "ptrace", "ig.com", "igamecj.com", "amsoveasea.com", "gcloudcs.com", "tss_get_report_data",
                      "tss_del_report_data", "tss_enable_get_report_data", "TssSDKGetReportData", "TssSDKDelReportData",
                      "tss_sdk_ischeatpacket", "tss_sdk_decryptpacket", "Java_com_tencent_tp_TssSdk_forceExit",
                      "killProcess"]

        replaced_value = int(0)

        try:
            for value in vals_bytes:
                replaced_value += self._MemTool_UTF8.read_write_value(str(value), "King")
        except Exception as e:
            print(self.C_WARNING + "[-] Exception occurred: ", e)

        print(self.C_GREEN + "[+] LBU-8: %d" % replaced_value)

    async def logo_bypass_offset(self):
        offsets_libanogs_DWORD = [0x000, 0xB80, 0xBB0, 0x59A4B0, 0x15D0, 0xAA980, 0x2F, 0x32B4, 0x50D63]
        offsets_libUE4_DWORD = [0x7E2A78, 0x7E2A80, 0x7E2A88]

        replaced_value = int(0)

        for offset in offsets_libanogs_DWORD:
            ret_values = self._MemTool_DWORD.write_lib(self._libanogs_base, offset, 1)
            if ret_values:
                replaced_value += 1

        for offset_Ue in offsets_libUE4_DWORD:
            ret_values = self._MemTool_DWORD.write_lib(self._libUE4_base, offset_Ue, 1)
            if ret_values:
                replaced_value += 1

        print(self.C_GREEN + "[+] LBO: %d" % replaced_value)

    async def logo_bypass_dword(self) -> None:
        vals_dword = [118334, 856896, 123010, 123179, 123274, 1026]

        replaced_value = int(0)
        try:
            for value in vals_dword:
                replaced_value += self._MemTool_DWORD.read_write_value(value, 1)
        except Exception as e:
            print(self.C_WARNING + "[-] Exception occurred: ", e)

        print(self.C_GREEN + "[+] LB-DSW: %d" % replaced_value)

    async def logo_bypass_float(self) -> None:
        vals_float = [9.21970312e-41, 13073.3740234375]

        replaced_value = int(0)
        try:
            for value in vals_float:
                replaced_value += self._MemTool_FLOAT.read_write_value(value, 0.1)
        except Exception as e:
            print(self.C_WARNING + "[-] Exception occurred: ", e)

        print(self.C_GREEN + "[+] LBF: %d" % replaced_value)

    async def lobby_bypass(self):
        offsets_libUE4_DWORD = [0x1D40C98, 0x1C57DEC, 0x1DBA718, 0x1d40c84, 0x1d1ddd4, 0x1c55c10, 0x1dba704, 0x1d40d48]

        replaced_value = int(0)
        for offset_Ue in offsets_libUE4_DWORD:
            ret_values = self._MemTool_FLOAT.write_lib(self._libUE4_base, offset_Ue, 0.1)
            if ret_values:
                replaced_value += 1

        print(self.C_GREEN + "[+] LBO: %d" % replaced_value)

    """-------------------------------------AntiCheat Patching Ending--------------------------------------------"""
    """-------------------------------------Basic Function --------------------------------------------"""

    async def no_recoil(self):
        """LibBase + offset = value   -> need to change"""
        recoil_offset_float = 0x1e85c74
        self._MemTool_FLOAT.write_lib(self._libUE4_base, recoil_offset_float, 4.55)

    async def speed_run(self):
        """LibBase + offset = value   -> need to change"""
        speed_offset_float = 0x27a5c80
        speed_offset_dword = 0x8a4fd48
        self._MemTool_FLOAT.write_lib(self._libUE4_base, speed_offset_float, 8.55015)
        self._MemTool_DWORD.write_lib(self._libUE4_base, speed_offset_dword, 400)

    """-------------------------------------Basic Function Ending--------------------------------------------"""
    """-------------------------------------Dumping Functions--------------------------------------------"""

    async def dump_map(self):
        is_dumped = self._MemTool_FLOAT.dump_maps(path="./")
        if is_dumped:
            print(self.C_GREEN + "[+] Map dumped of process %s is found in %s" % (self._PID, getcwd()))
        else:
            print(self.C_FAIL + "[-] Unable to dump maps")

    """-------------------------------------Dumping Functions Ending--------------------------------------------"""
    """-------------------------------------Main Menu Function --------------------------------------------"""

    async def lobby_work(self) -> None:
        while True:
            print(self.C_BLUE + "[+] 1. Lobby Anti-Cheat System")
            print(self.C_BLUE + "[+] 2. No Recoil")
            print(self.C_BLUE + "[+] 3. Speed Run")
            print(self.C_BLUE + "[+] 4. Dump Maps")
            print(self.C_BLUE + "[+] 5. Exit and release memory")
            ans = input(self.C_BOLD + self.C_CYAN + ">>>> ")
            ans = int(ans)
            if ans == 1:
                await self.lobby_bypass()
            elif ans == 2:
                await self.no_recoil()
            elif ans == 3:
                await self.speed_run()
            elif ans == 4:
                await self.dump_map()
            elif ans == 5:
                exit(0)
            else:
                print(self.C_FAIL + "[+] Choose given options")
                await sleep(2)

    """-------------------------------------Main Menu Function Ending--------------------------------------------"""
    """-------------------------------------Main Function --------------------------------------------"""

    def get_ticks(self):
        self._event_loop.run_until_complete(self.__async__get_ticks())


if __name__ == '__main__':
    py_cheats_object = PyCheats()
    py_cheats_object.get_ticks()
