#!/usr/bin/env python
import pyautogui
import os
import sys
import json
import argparse
import time
from pathlib import Path

def get_root_dir():
    return sys.path[0]

def get_client_base_dir():
    global_config = load_global_config_file()
    spaces = global_config.keys()

    current_path = initial_path = Path(os.getcwd())

    while current_path.parts[-1] not in spaces:
        parent = current_path.parent
        if parent == current_path:
            current_path = initial_path
            break
        current_path = parent
    return current_path.as_posix()

def get_client_base_folder_name():
    return os.path.basename(get_client_base_dir())

def load_global_config_file():
    path = get_root_dir() + "\\global_config.json"
    with open(path, "r+") as f:
        config = json.load(f)
        return config

def save_to_global_config_file(new_config):
    path = get_root_dir() + "\\global_config.json"

    config = load_global_config_file()
    with open(path, "w+") as f:
        config[new_config.pop("name")] = new_config
        json.dump(config, f)

def save_global_config_file(new_config):
    path = get_root_dir() + "\\global_config.json"

    with open(path, "w+") as f:
        json.dump(new_config, f)

def load_client_config_file():
    path = get_client_base_dir() + "\\.space-dev-config"

    try:
        with open(path, "r") as f:
            config = json.load(f)
            return config
    except:
        print(f"[space-dev] Unable to load {path} file on current directory.")
        sys.exit()

def add_space():
    config = load_client_config_file()
    generated_gobal_config = {}

    # name check
    if "name" in config.keys():
        space_name = config["name"]
    else:
        space_name = get_client_base_folder_name()

    generated_gobal_config["name"] = space_name

    # path check
    if "path" in config.keys():
        path = config.pop("path")
    else:
        path = get_client_base_dir()

    generated_gobal_config["path"] = path

    # run command check
    if "run" in config.keys():
        generated_gobal_config["run"] = config.pop("run")

    # get extra parameters
    for key in config.keys():
        generated_gobal_config[key] = config[key]

    save_to_global_config_file(generated_gobal_config)

def list_spaces():
    global_config = load_global_config_file()
    
    for i, space in enumerate(global_config.keys()):
        print(str(i) + ". " + space)

def exec_space(space_name, run=None, load=False):
    global_config = load_global_config_file()

    try:
        space_config = global_config[space_name]
    except:
        print("[space-dev] The space name was not found")
        list_spaces()
        return False
    
    # get path
    path = space_config["path"]

    # cd to path
    os.chdir(path)

    commands = None

    program = os.getenv("TERM_PROGRAM")

    if run == None and program in space_config.keys():
        commands = space_config[program]

        # check if is an integrated terminal
        if program == "vscode":
            for cmd in commands:
                pyautogui.keyDown('ctrl')
                pyautogui.keyDown('shift')
                pyautogui.keyDown('`')
                pyautogui.keyUp('ctrl')
                pyautogui.keyUp('shift')
                pyautogui.keyUp('`')

                time.sleep(1.5)

                pyautogui.press("enter")
                pyautogui.typewrite(cmd)
                pyautogui.press("enter")
    
    elif run:
        if "scripts" in space_config.keys():
            scripts = space_config["scripts"]
            if run in scripts.keys():
                commands = space_config["scripts"][run]
            else:
                print(f"[space-dev] Unable to find {run} on 'scripts'. Try running 'space-dev run --ls' for a list of avaible scripts.")
                sys.exit()
        else:
            print(f"[space-dev] Unable to find 'scripts' section on '.space-dev-config' file.")

    # exec run commands
    elif load:
        commands = space_config["run"]

    for cmd in commands:
        os.system(cmd)

    return True

def get_space_name_from_number(number):
    global_config = load_global_config_file()
    return list(global_config.keys())[number]

def remove_space(space):
    global_config = load_global_config_file()

    if space in global_config.keys():
        global_config.pop(space)
        save_global_config_file(global_config)
        print(f"[space-dev] The space {space} was removed.")
    else:
        print("[space-dev] The space could not be removed because it does not exit.")

def list_scripts():
    global_config = load_global_config_file()
    space_config = global_config[get_client_base_folder_name()]
    scripts = space_config["scripts"]

    for script in scripts.keys():
                print(script)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Saves and auto opens your development space')

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = False

    loadparser = subparsers.add_parser("load")
    loadparser.add_argument('load', nargs=1, help="Load space")

    lsparser = subparsers.add_parser("ls")
    lsparser.add_argument('ls', action="store_true", help="List spaces")

    rmparser = subparsers.add_parser("rm")
    rmparser.add_argument('rm', nargs=1, help="Remove space")

    runparser = subparsers.add_parser("run")
    runparser.add_argument('run', nargs="?", help="Run aditional scripts.")
    runparser.add_argument('--ls', action="store_true",help="List scripts to run")

    args = parser.parse_args()



    # list spaces
    if args.command == "ls":
        list_spaces()
        sys.exit()
    
    # remove space
    if args.command == "rm":
        remove_space(args.rm[0])
        sys.exit()

    if args.command == "run":
        if args.ls:
            list_scripts() 
            sys.exit()
    
        exec_space(get_client_base_folder_name(), run=args.run)
        sys.exit()

    if args.command == "load":
        space_name = args.load[0]
        # check if the space number was provided
        try:
            space_number = int(space_name)
            space_name = get_space_name_from_number(space_number)
        except:
            pass

        print("[space-dev] Executing space " + str(space_name))
        exec_space(space_name, load=True)
        sys.exit()

    if args.command == None:
        add_space()
        print("[space-dev] Adding space...")
