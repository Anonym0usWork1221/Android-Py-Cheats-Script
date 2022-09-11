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
