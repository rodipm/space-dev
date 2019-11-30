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
    path = Path(get_client_base_dir(), ".space-dev-config")

    try:
        with open(path, "r") as f:
            config = json.load(f)
            return config
    except:
        print(f"[space-dev] Unable to load {path} file on current directory.")
        sys.exit()


def add_space():
    global_config = load_global_config_file()
    config = load_client_config_file()
    generated_gobal_config = {}
    is_new_space = None

    # name check
    if "name" in config.keys():
        space_name = config["name"]
    else:
        space_name = get_client_base_folder_name()

    generated_gobal_config["name"] = space_name

    # verify if space already exists
    if space_name in global_config.keys():
        is_new_space = False
    else:
        is_new_space = True

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

    return is_new_space


def list_spaces():
    global_config = load_global_config_file()

    for i, space in enumerate(global_config.keys()):
        print(str(i) + ". " + space)

def start_space():
    space_config = load_client_config_file()

    program = os.getenv("TERM_PROGRAM")

    if "start" not in space_config.keys():
        print("[space-dev] There are no start scripts for this space.")
        sys.exit()

    if program in space_config["start"].keys():
        commands = space_config["start"][program]

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
    else:
        print(f"[space-dev] There is no start script linked to {program} for this space.")

def exec_space(space_name, run=None, load=False):
    global_config = load_global_config_file()

    try:
        space_config = global_config[space_name]
    except:
        print("[space-dev] The space name was not found")
        list_spaces()
        sys.exit()

    # get path
    path = space_config["path"]

    # cd to path
    os.chdir(path)

    commands = None

    if run:
        if "scripts" in space_config.keys():
            scripts = space_config["scripts"]

            # check if a script number was provided
            try:
                script_number = int(run)
                run = get_script_name_from_number(script_number)
            except:
                pass

            if run in scripts.keys():
                commands = space_config["scripts"][run]
            else:
                print(
                    f"[space-dev] Unable to find {run} on 'scripts'. Try running 'space-dev run --ls' for a list of avaible scripts.")
                sys.exit()
        else:
            print(
                f"[space-dev] Unable to find 'scripts' section on '.space-dev-config' file.")
            sys.exit()

    # exec run commands
    elif load:
        commands = space_config["run"]

    for cmd in commands:
        os.system(cmd)

    return True


def get_space_name_from_number(number):
    global_config = load_global_config_file()
    return list(global_config.keys())[number]


def get_script_name_from_number(number):
    client_config = load_client_config_file()
    return list(client_config["scripts"].keys())[number]

def remove_space(space):
    global_config = load_global_config_file()

    try:
        space_number = int(space)
        space = get_space_name_from_number(space_number)
    except:
        pass

    if space in global_config.keys():
        global_config.pop(space)
        save_global_config_file(global_config)
        print(f"[space-dev] The space {space} was removed.")
    else:
        print("[space-dev] The space could not be removed because it does not exit.")


def list_scripts():
    global_config = load_global_config_file()
    space_config = global_config[get_client_base_folder_name()]

    if "scripts" in space_config.keys():
        scripts = space_config["scripts"]
    else:
        print("There are no scripts for this space.")
        return False

    for i, script in enumerate(scripts.keys()):
        print(str(i) + ". " + script)


def list_start_scripts():
    space_config = load_client_config_file()

    if "start" in space_config.keys():
        scripts = space_config["start"]
        for i, script in enumerate(scripts):
            print(str(i) + ". " + script)
    else:
        print("There are no start scripts for this space.")
        sys.exit()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Saves and auto opens your development space')

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = False

    addparser = subparsers.add_parser("add")
    addparser.add_argument('add', action="store_true",
                           help="Add (or updates) a space. Can be used from any space subdirectory.")

    loadparser = subparsers.add_parser("load")
    loadparser.add_argument('load', nargs=1, help="Load space")

    startparser = subparsers.add_parser("start")
    startparser.add_argument('start', action="store_true", help="Start space's application specific scripts")
    startparser.add_argument('--ls', action="store_true",
                           help="List space's application specific scripts to start")

    runparser = subparsers.add_parser("run")
    runparser.add_argument('run', nargs="?", help="Run aditional scripts.")
    runparser.add_argument('--ls', action="store_true",
                           help="List scripts to run")

    lsparser = subparsers.add_parser("ls")
    lsparser.add_argument('ls', action="store_true", help="List spaces")

    rmparser = subparsers.add_parser("rm")
    rmparser.add_argument('rm', nargs=1, help="Remove space")


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
        else:
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

        exec_space(space_name, load=True)
        print("[space-dev] Executing space " + str(space_name))
        sys.exit()

    if args.command == "add":
        is_new_space = add_space()

        if is_new_space:
            print("[space-dev] Adding space...")
        else:
            print("[space-dev] Updating space...")

        sys.exit()
    
    if args.command == "start":
        if args.ls:
            list_start_scripts()
        else:
            start_space()
        sys.exit()

    if args.command == None:
        parser.print_help()
        sys.exit()
