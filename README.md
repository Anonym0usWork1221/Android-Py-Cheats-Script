Android-Py-Cheats-Script
====
[![GitHub stars](https://img.shields.io/github/stars/Anonym0usWork1221/Android-Py-Cheats-Script.svg)](https://github.com/Anonym0usWork1221/Android-Py-Cheats-Script/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Anonym0usWork1221/Android-Py-Cheats-Script.svg)](https://github.com/Anonym0usWork1221/Android-Py-Cheats-Script/network/members)
[![GitHub issues](https://img.shields.io/github/issues/Anonym0usWork1221/Android-Py-Cheats-Script.svg)](https://github.com/Anonym0usWork1221/Android-Py-Cheats-Script/issues)
[![GitHub watchers](https://img.shields.io/github/watchers/Anonym0usWork1221/Android-Py-Cheats-Script.svg)](https://github.com/Anonym0usWork1221/Android-Py-Cheats-Script/watchers)
[![Python](https://img.shields.io/badge/language-Python%203-blue.svg)](https://www.python.org)
[![GPT_LICENSE](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/)

-----------


**This is am example of using androidMemoryTool on android
This script is generated for game pubg mobile.
Can be use in Fortnite and other games for cheats**

If you find any bug or not working function you can contact me. 

 *  Author : Abdul Moez
 *  Study  : UnderGraduate in GCU Lahore, Pakistan
 *  Repo  :(https://github.com/Anonym0usWork1221/Android-Py-Cheats-Script)
 
 MIT License

 Copyright (c) 2022 AbdulMoez


Requirments
-----------
* Link to repo android memory tool (https://github.com/Anonym0usWork1221/android-memorytool)
* Install the requirements.txt file ```pip install -r requirements.txt```

* Needed python version 3.x

* Android Requirments -> Rooted Device Needed

* Requirements and root automatically acquire just start script

* ``` python3 PyCheats.py ```

Documentation, Installation
----------------------------------------
* **__Installation__**  
  **Simply run PyCheats.py it will automatically install requirements**

* **__Documentation__**
  1. First of I imported the required packages. The module **InfoCollector** is custom module  
   the try except blocks are used inorder to detect that these modules are installed if not  
   then install then first.  

  ```py
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
  ```

  2. Simply added lambda function for clearing the terminal

  ```py
  clear = lambda: os.system("clear")
  ```

  3. Create class and initialize required variables

  ```py
  class MemoryTools:
    pkg = None
    PID = None
    data = None
    libanogs_base = 0x0
    libUE4_base = 0x0
    is64 = None
    lib_libanogs = None
  ```

  4. Set up init function and run different functions on startup of that function.

  ```py
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
  ```

  5. Function **is_rooted_acquired** check if the script is running as root or not

  ```py
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
  ```

  6. Function **upack_information** checking information stored in gameInfo.txt file  
     Like __package name__ and __libs path__

  ```py
  @staticmethod
    def upack_information() -> tuple[str, str]:
        with open("gameInfo.txt", 'r') as f:
            d = f.read()
            f.close()
        file_data = d.split()
        pkg_name = file_data[0]
        data_path = file_data[1]
        return pkg_name, data_path
  ```

  7. Function **decoration** is used for displaying name text for styling

  ```py
    @staticmethod
      def decoration():
          clear()
          print("[*] Welcome to Example Script by Anonym0usWork1221\nhttps://github.com/Anonym0usWork1221\n\n")
  ```

  8. Function **is64_version** is asking for package name and version from user and   
     storing in **gameInfo.txt** file for latter use.

  ```py
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
  ```

  9. Function **is_game_running** is checking that if game running and setting up **PID** variable

  ```py
      def is_game_running(self) -> bool:
        self.PID = androidMemoryTool.get_pid(self.pkg)
        if not self.PID == "":
            return True
        else:
            return False
  ```

  10. Function **logo_bypass_utf8** is searching utf-8 strings and changing them using AndroidMemoryTool  
      ```py 
      androidMemoryTool.SettingUpTool().init_setup(PKG=self.pkg, TYPE=androidMemoryTool.DataTypes.UTF_8, 
                                                    SPEED_MODE=True, WORKERS=100)    
      ```
      Here we are setting up the androidMemoryTool by giving **package name** (provided by user), **DataType**  
      (UTF_8 in this case), **SPEED_MODE** (To use speed algorithms in speeding up Search), and **WORKERS** (number of works used to speed up)  

      ```py
      androidMemoryTool.InitMemoryTool().init_tool(pMAP=androidMemoryTool.PMAP(ALL=False, CODE_APP=True))
      ```
      Here we are initializing the androidMemoryTool by giving maps range we want to use.

  ```py
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
  ```

  11. Function **logo_bypass_offset** is writing the value of offsets directly

  ```py
      def logo_bypass_offset(self):
        offsets_libanogs_DWORD = [0x000, 0xB80, 0xBB0, 0x59A4B0, 0x15D0, 0xAA980, 0x2F, 0x32B4, 0x50D63]
        offsets_libUE4_DWORD = [0x7E2A78, 0x7E2A80, 0x7E2A88]

        for offset in offsets_libanogs_DWORD:
            androidMemoryTool.write_lib_offsets_DWORD(self.PID, self.libanogs_base, offset, 0)

        for offset_Ue in offsets_libUE4_DWORD:
            androidMemoryTool.write_lib_offsets_DWORD(self.PID, self.libUE4_base, offset_Ue, 0)
        print("[*] Logo_bypass_offset: Completed")
  ```

  12. Function **Below** have same work in creating anti cheat system.

  ```py
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
  ```

  13. Functions **no_recoil, speed_run** are sample function (address not working) used for  
      No recoil address writing, and speed runing of player. 

  ```py
      def no_recoil(self):
        """LibBase + offset = value   -> need to change"""
        androidMemoryTool.write_lib_offsets_FLOAT(self.PID, self.libUE4_base, 0x1e85c74, 4.55)

      def speed_run(self):
        """LibBase + offset = value   -> need to change"""
        androidMemoryTool.write_lib_offsets_FLOAT(self.PID, self.libUE4_base, 0x27a5c80, 8.55015)
        androidMemoryTool.write_lib_offsets_DWORD(self.PID, self.libUE4_base, 0x8a4fd48, 400)
  ```

  14. Function **lobby_work** is used in controlling functions in loop

  ```py
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
  ```

  15. Executing **MemoryTools**

  ```py
      if __name__ == '__main__':
        MemoryTools().__int__()
  ```

  15. Other File **InfoCollector** is used for reading and writing __gameInfo.txt__ file

  ```py
    import os

    def compare() -> bool:
        with open("gameInfo.txt", 'r') as f:
            data = f.read()
            f.close()
        all = data.split()
        if data == "":
            return False
        if os.path.exists("/storage/emulated/0/Android/data/{}".format(all[0])):
            if os.path.exists(all[1]):
                return True
            else:
                return False
        else:
            return False


    def get_data() -> None:
        while not compare():
            pkg = input("[x] Enter package name: ")
            data = input("[x] Enter data path: ")
            with open("gameInfo.txt", 'w') as f:
                f.write(f"{pkg}\n{data}")
                f.close()

  ```

# Video Demonstration
**Video Demonstration for using AndroidMemoryTool**

[![usage](https://img.youtube.com/vi/vebE1Rf1ogo/0.jpg)](https://www.youtube.com/watch?v=vebE1Rf1ogo)


Supported Data Types
-------------------
All data types are signed.

| **Range** | **Name** |  **Ctype** |
| ------- | -------- | ------------|
| -2,147,483,648 to 2,147,483,647 | DWORD | signed int 
| 3.4E +/- 38 (7 digits) | FLOAT | float
| 1.7E +/- 308 (15 digits) | DOUBLE | double
| -32,768 to 32,767 | WORD | signed short int
| -128 to 127 | BYTE | signed char
| -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 | QWORD | signed long long
| -2,147,483,648 to 2,147,483,647 | XOR | signed long
| Random | UTF-8 | Text
| Random | UTF-16LE | Text
  

* Supported Maps Ranges

--------------------
| **Short Name** | **Name** |  **Description** |
| ------- | -------- | ------------|
| ALL | Whole Memory | Whole Memory of current process (slow)
| CA | C++ alloc | RAM c++ Allocated memory
| A  | Anonymous | Range with r-w access only
| Xa | Code App  | shared libs memory (dangerous)
|Jh|Java Heap| Java heap
|Ch|C++ Heap| Heap memory of cpp
|Cd|C++ .data| .Data Memory
|Cb|C++ .bss| .bss section memory
|J|Java| Java memory section
|S|Stack| Stack Memory
|As|Ashmen| Ashmen Memory
|V|Video| Video memory range 
|B_Bad|Bad| Bad Memory (dangerous)
|Xs|Code system| Code system memory (dangerous)


# Contributor

<a href = "https://github.com/Anonym0usWork1221/Android-Py-Cheats-Script/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=Anonym0usWork1221/Android-Py-Cheats-Script"/>
</a>


Assistance
----------
If you need assistance, you can ask for help on my mailing list:

* Email      : abdulmoez123456789@gmail.com

I also created a Discord group:

* Server     : https://discord.gg/RMNcqzmt9f


Buy Me a coffe
--------------
If you want to support me you can buy me coffe.

BitCoin_addr: ``` 19vwfRXfthPY7f2aqDBpxQvZa6AJFKcdBS ```
