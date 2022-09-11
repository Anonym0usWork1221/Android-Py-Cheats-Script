#! /usr/bin/env python
import sys
import os
import time
import InfoCollector
import subprocess

try:
    import androidMemoryTool
    from rich import print
    from androidMemoryTool import AndroidMemoryTool
except ImportError:
    print("[*] Installing requirements")
    os.system("pip3 install -r ./requirements.txt")
    subprocess.call(['sudo', 'python3', *sys.argv])
    sys.exit(1)

clear = lambda: os.system("clear")


class MemoryTools:
    pkg = None
    PID = None
    data = None
    libanogs_base = 0x0
    libUE4_base = 0x0
    is64 = None
    lib_libanogs = None

    def __int__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_rooted_acquired()
        self.decoration()

        # Grabbing ids
        self.pkg, self.data, self.is64 = self.is64_version()

        # checking is game running and getting pid
        if self.is_game_running():
            print("[*] Game Running.")
        else:
            print("[*] Game PID not found.")
            sys.exit()

        """Getting Base address"""
        self.libanogs_base = androidMemoryTool.get_module_base_address(self.PID, "libanogs.so")
        self.libUE4_base = androidMemoryTool.get_module_base_address(self.PID, "libUE4.so")

        print("[*] Security dispatching Started")
        self.logo_bypass_utf8()
        self.logo_bypass_offset()
        self.logo_bypass_dword()
        self.logo_bypass_float()
        print("[*] Security dispatching Completed")

        time.sleep(2)

        self.decoration()
        self.lobby_work()

    @staticmethod
    def is_rooted_acquired():
        if os.getuid() != 0:
            print("[*] Root Required")
            print("[*] Rebooting script as root")
            time.sleep(2)
            subprocess.call(['sudo', 'python3', *sys.argv])
            sys.exit(1)
        else:
            print("Root Acquired")

    @staticmethod
    def upack_information() -> tuple[str, str]:
        with open("gameInfo.txt", 'r') as f:
            d = f.read()
            f.close()
        file_data = d.split()
        pkg_name = file_data[0]
        data_path = file_data[1]
        return pkg_name, data_path

    @staticmethod
    def decoration():
        # clear()
        print("[*] Welcome to Example Script by Anonym0usWork1221\nhttps://github.com/Anonym0usWork1221\n\n")

    def is64_version(self) -> tuple[str, str, bool]:
        print("\n[*] 1. 32 bits")
        print("[*] 2. 64 bits")
        while True:
            try:
                bits_type = int(input("[*] Choose pubg bits: "))
                break
            except Exception as e:
                print(e)
        if bits_type == 1:
            while not InfoCollector.compare():
                pkg_name = input("Enter package name: ")
                data = input("Enter Libs Path: ")

                with open("gameInfo.txt", 'w') as gameInfoWriter:
                    gameInfoWriter.write(f"{pkg_name}\n{data}")
                    gameInfoWriter.close()

            pkg_name, data = self.upack_information()
            return pkg_name, data, False
        else:
            InfoCollector.get_data()
            pkg_name, data = self.upack_information()
            return pkg_name, data, True

    def is_game_running(self) -> bool:
        self.PID = androidMemoryTool.get_pid(self.pkg)
        if not self.PID == "":
            return True
        else:
            return False

    def logo_bypass_utf8(self) -> None:
        vals_bytes = ["libUE4.so", "libBugly.so", "libanogs.so", "l_report", "get_report", "tss_sdk_rcv_anti_data",
                      "AreaData.dat",
                      "AntiCheatData", "Reports", "hack", "ban", "cheat", "qq.com", "packets.com",
                      "killProcess"]

        androidMemoryTool.SettingUpTool().init_setup(PKG=self.pkg, TYPE=androidMemoryTool.DataTypes.UTF_8,
                                                     SPEED_MODE=True, WORKERS=100)

        # set True to maps you want to use
        androidMemoryTool.InitMemoryTool().init_tool(pMAP=androidMemoryTool.PMAP(ALL=False, CODE_APP=True))

        replaced_value = 0
        try:
            for value in vals_bytes:
                replaced_value += AndroidMemoryTool.read_write_value(str(value), "AbdulMoez")
        except Exception as e:
            print(e)

        print("[*] Logo_bypass_utf8: " + str(replaced_value))

    def logo_bypass_offset(self):
        offsets_libanogs_DWORD = [0x000, 0xB80, 0xBB0, 0x59A4B0, 0x15D0, 0xAA980, 0x2F, 0x32B4, 0x50D63]
        offsets_libUE4_DWORD = [0x7E2A78, 0x7E2A80, 0x7E2A88]

        for offset in offsets_libanogs_DWORD:
            androidMemoryTool.write_lib_offsets_DWORD(self.PID, self.libanogs_base, offset, 0)

        for offset_Ue in offsets_libUE4_DWORD:
            androidMemoryTool.write_lib_offsets_DWORD(self.PID, self.libUE4_base, offset_Ue, 0)

        print("[*] Logo_bypass_offset: Completed")

    def logo_bypass_dword(self) -> None:
        vals_dword = [118334, 856896, 123010, 123179, 123274, 1026]
        androidMemoryTool.SettingUpTool().init_setup(PKG=self.pkg, TYPE=androidMemoryTool.DataTypes.DWORD,
                                                     SPEED_MODE=True, WORKERS=100)

        androidMemoryTool.InitMemoryTool().init_tool(pMAP=androidMemoryTool.PMAP(ALL=False, CODE_APP=True))

        replaced_value = 0
        try:
            for value in vals_dword:
                replaced_value += AndroidMemoryTool.read_write_value(value, 1)
        except Exception as e:
            print(e)

        print("[*] logo_bypass_dword: " + str(replaced_value))

    def logo_bypass_float(self) -> None:
        vals_float = [9.21970312e-41, 13073.3740234375, 2.2958874e-41]
        androidMemoryTool.SettingUpTool().init_setup(PKG=self.pkg, TYPE=androidMemoryTool.DataTypes.FLOAT,
                                                     SPEED_MODE=False, WORKERS=55)

        androidMemoryTool.InitMemoryTool().init_tool(pMAP=androidMemoryTool.PMAP(CODE_APP=True, ALL=False))

        replaced_value = 0
        try:
            for value in vals_float:
                replaced_value += AndroidMemoryTool.read_write_value(value, 0.1)
        except Exception as e:
            print(e)

        print("[*] logo_bypass_float: " + str(replaced_value))

    def lobby_bypass(self):
        offsets_libUE4_DWORD = [0x1D40C98, 0x1C57DEC, 0x1DBA718, 0x1d40c84, 0x1d1ddd4, 0x1c55c10, 0x1dba704, 0x1d40d48]

        for offset_Ue in offsets_libUE4_DWORD:
            androidMemoryTool.write_lib_offsets_FLOAT(self.PID, self.libUE4_base, offset_Ue, 0.1)

        print("[*] lobby_bypass: 8")

    def logo_arm_bypass(self) -> None:
        # Based on arm instructions (not available yet)
        pass

    def no_recoil(self):
        """LibBase + offset = value   -> need to change"""
        androidMemoryTool.write_lib_offsets_FLOAT(self.PID, self.libUE4_base, 0x1e85c74, 4.55)

    def speed_run(self):
        """LibBase + offset = value   -> need to change"""
        androidMemoryTool.write_lib_offsets_FLOAT(self.PID, self.libUE4_base, 0x27a5c80, 8.55015)
        androidMemoryTool.write_lib_offsets_DWORD(self.PID, self.libUE4_base, 0x8a4fd48, 400)

    def lobby_work(self) -> None:
        while True:
            print("[*] 1. Lobby Anti-Cheat System")
            print("[*] 2. No Recoil")
            print("[*] 3. Speed Run")
            print("[*] 4. Exit and release memory")
            ans = input(">>>> ")
            ans = int(ans)
            if ans == 1:
                self.lobby_bypass()
            elif ans == 2:
                self.no_recoil()
            elif ans == 3:
                self.speed_run()
            elif ans == 4:
                sys.exit(0)
            else:
                print("[*] Choose given options")
                time.sleep(2)


if __name__ == '__main__':
    MemoryTools().__int__()
