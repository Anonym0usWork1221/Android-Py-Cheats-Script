from os import path
from json import loads, dump


async def compare() -> bool:
    if not path.isfile("process_info.json"):
        return False

    with open("process_info.json", 'r') as json_file:
        current_info = loads(json_file.read())
        json_file.close()

    game_package_name = current_info["game_pkg"]

    if game_package_name == "":
        return False

    elif path.exists("/storage/emulated/0/Android/data/{}".format(game_package_name)):
        return True

    else:
        print("[-] Package Not found. Please type again or press ctrl+c to exit.")
        return False


async def get_data() -> None:
    while not (await compare()):
        pkg_name = input("[x] Enter package name: ")
        process_info = {"game_pkg":  pkg_name}
        dump(process_info, open("process_info.json", "w"))
