#!/usr/bin/env python3
import winreg
import os
import importlib


def choose_key(write=False):
    param = []
    param = [winreg.HKEY_CURRENT_USER, "Environment"]
    if write:
        param.extend([0, winreg.KEY_ALL_ACCESS])
    return winreg.OpenKey(*param)


def get_path():
    key = choose_key()
    path = winreg.QueryValueEx(key, 'path')[0]
    return path.strip()


def add_to_path():
    current_path = get_path()
    target_path = os.getcwd()

    if target_path.lower() in current_path.lower():
        print("[space-dev] Local directory already in path!")
        return

    key = choose_key(write=True)

    current_path = (
        current_path + ';') if not current_path.endswith(';') else current_path
    new_path = current_path + target_path

    winreg.SetValueEx(key, "path", 0, winreg.REG_EXPAND_SZ, new_path)

    print("[space-dev] Local directory added to path!")


def install_packages():
    with open("requirements.txt", "r") as f:
        packages = f.readlines()
        for pck in packages:
            pck = pck.rstrip('\n')
            print(pck)
            importlib.import_module(pck)




def main():
    add_to_path()
    install_packages()


if __name__ == '__main__':
    main()
