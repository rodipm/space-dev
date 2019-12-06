#!/usr/bin/env python3
import os
import importlib
from platform import system
import re
import requests
import tqdm

if system() == "Windows":
    import winreg



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
    if system() == "Windows":
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
    
    else:
        p = re.compile("PATH=\"(.+)\"")

        current_dir = os.getcwd()

        old_env = open("/etc/environment", "r").read()

        if current_dir in old_env:
            print("[space-dev] Local directory already in path!")
            return

        try:
            old_path = p.findall(old_env)[0]
            new_env = old_env.replace("PATH=\"" + old_path + "\"", '')
        except IndexError:
            old_path = ""
            new_env = old_env

        new_path = old_path + ":" + current_dir
        new_env = "PATH=\"" + new_path + "\"" + new_env

        try:
            with open("/etc/environment", "w") as env:
                env.write(new_env)
        except PermissionError:
            print("[space-dev] Please run this installation script with sudo!")
            return

    print("[space-dev] Local directory added to path!")


def install_packages():
    with open("requirements.txt", "r") as f:
        packages = f.readlines()
        for pck in packages:
            pck = pck.rstrip('\n')
            print(pck)
            importlib.import_module(pck)

def download_release():
    r = requests.get("https://github.com/rodipm/space-dev/releases/download/0.1/space_dev")
    with open("space_dev", "wb+") as f:
        f.write(r.content)

def main():
    download_release()
    add_to_path()
    # install_packages()

if __name__ == '__main__':
    main()