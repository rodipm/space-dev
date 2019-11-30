#!/usr/bin/env python3
import pyautogui
import os
import sys
import json
import argparse
import time
from pathlib import Path
import re

#####################################################################
#####################################################################
#####                           DIR                             #####
#####################################################################
#####################################################################

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
    path = get_root_dir() + "/global_config.json"
    with open(path, "r+") as f:
        config = json.load(f)
        return config

def save_global_config_file(new_config, update=False):
    path = get_root_dir() + "/global_config.json"

    with open(path, "w+") as f:
        if update:
            config = load_global_config_file()
            config[new_config.pop("name")] = new_config
            json.dump(config, f)
        else:
            with open(path, "w+") as f:
                json.dump(new_config, f)

def load_client_config_file():
    path = Path(get_client_base_dir(), ".space-dev-config.json")

    try:
        with open(path, "r") as f:
            config = json.load(f)
            return config
    except json.JSONDecodeError as err:
        print(f"[space-dev] Unable to parse .space-dev-config.json.")
        print(err)
    except:
        print(f"[space-dev] Unable to load {path} file on current directory.")
    sys.exit()

#####################################################################
#####################################################################
#####                          LISTS                            #####
#####################################################################
#####################################################################

def list_spaces(show=True):
    global_config = load_global_config_file()
    spaces = global_config.keys()
    if show:
        print("[space-dev] Spaces available:")
        for i, space in enumerate(spaces):
            print(str(i) + ". " + space)
    return spaces

def list_scripts():
    space_config = load_client_config_file()

    if "scripts" in space_config.keys():
        scripts = space_config["scripts"]
    else:
        print("[space-dev] There are no scripts for this space.")
        return False

    print("[space-dev] Scripts for this space:")
    for i, script in enumerate(scripts.keys()):
        print(str(i) + ". " + script)


def list_start_scripts():
    space_config = load_client_config_file()

    if "start" in space_config.keys():
        scripts = space_config["start"]
        print("[space-dev] Start scripts for this space:")
        for i, script in enumerate(scripts):
            print(str(i) + ". " + script)
    else:
        print("[space-dev] There are no start scripts for this space.")
        sys.exit()

def list_load_scripts(space_name):
    global_config = load_global_config_file()
    space_config = None
    try:
        space_config = global_config[space_name]
    except:
        print("[space-dev] The space name was not found.")
        sys.exit()

    if "load" in space_config.keys():
        scripts = space_config["load"]

        print("[space-dev] Load scripts for this space:")
        for i, script in enumerate(scripts):
            print(str(i) + ". " + script)
    else:
        print("[space-dev] There are no load scripts for this space.")
        sys.exit()

#####################################################################
#####################################################################
#####                      FROM NUMBER                          #####
#####################################################################
#####################################################################


def parse_space_name(number):
    global_config = load_global_config_file()
    try:
        number = int(number)
        return list(global_config.keys())[number]
    except:
        pass

def parse_script_name(number):
    client_config = load_client_config_file()
    try:
        number = int(number)
        return list(client_config["scripts"].keys())[number]
    except:
        pass

def parse_load_script_name(number):
    client_config = load_client_config_file()
    try:
        number = int(number)
        return list(client_config["load"].keys())[number]
    except:
        pass

#####################################################################
#####################################################################
#####                      SPACE MNGMNT                         #####
#####################################################################
#####################################################################

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
    if "load" in config.keys():
        generated_gobal_config["load"] = config.pop("load")

    # get extra parameters
    for key in config.keys():
        generated_gobal_config[key] = config[key]

    save_global_config_file(generated_gobal_config, update=True)

    return is_new_space

def load_space(space_name, load_script=0):
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

    # exec run commands
    if load_script:
        commands = space_config["load"][load_script]
    else:
        first_key = list(space_config["load"].keys())[0]
        commands = space_config["load"][first_key]

    for cmd in commands:
        os.system(cmd)

    return True

def start_space():
    space_config = load_client_config_file()

    # check if is an integrated terminal
    program = os.getenv("TERM_PROGRAM")
    if not program and os.getenv("TMUX"):
        program = "TMUX"

    if "start" not in space_config.keys():
        print("[space-dev] There are no start scripts for this space.")
        sys.exit()

    if program in space_config["start"].keys():
        commands = space_config["start"][program]

        for cmd in commands:
            cmd, keys = parse_commands(cmd)

            for key in keys:
                pyautogui.keyDown(key)
            for key in reversed(keys):
                pyautogui.keyUp(key)

            if cmd:
                time.sleep(1.5)

                pyautogui.press("enter")
                pyautogui.typewrite(cmd)
                pyautogui.press("enter")
    else:
        print(
            f"[space-dev] There is no start script linked to {program} for this space.")


def run_script(space_name, run=None, load=False, load_script=0):
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

    if "scripts" in space_config.keys():
        scripts = space_config["scripts"]

        # check if a script number was provided

        run = parse_script_name(script_number)


        if run in scripts.keys():
            commands = space_config["scripts"][run]
        else:
            print(
                f"[space-dev] Unable to find {run} on 'scripts'. Try running 'space-dev run --ls' for a list of avaible scripts.")
            sys.exit()
    else:
        print(
            f"[space-dev] Unable to find 'scripts' section on '.space-dev-config.json' file.")
        sys.exit()

    for cmd in commands:
        os.system(cmd)

    return True

def remove_space(space):
    global_config = load_global_config_file()

    try:
        space_number = int(space)
        space = parse_space_name(space_number)
    except:
        pass

    if space in global_config.keys():
        global_config.pop(space)
        save_global_config_file(global_config)
        print(f"[space-dev] The space {space} was removed.")
    else:
        print("[space-dev] The space could not be removed because it does not exit.")

def parse_commands(command):
    cmd = command
    p = re.compile('<<(.+)>>')
    sequence = p.findall(command)

    if len(sequence):
        sequence = sequence[0]
        cmd = cmd.replace('<<'+sequence+'>>', '')
        sequence = sequence.split('+')
        return cmd, sequence

    else:
        return cmd, None

#####################################################################
#####################################################################
#####                         MAIN                              #####
#####################################################################
#####################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Saves and auto opens your development space')

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = False

    addparser = subparsers.add_parser("add")
    addparser.add_argument('add', action="store_true",
                           help="Add (or updates) a space. Can be used from any space subdirectory.")

    loadparser = subparsers.add_parser("load")
    loadparser.add_argument('load', nargs='*', help="Load space")
    loadparser.add_argument('--ls', action="store_true",
                           help="List space's load  scripts")

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

    #####################################################################
    #####                         ADD                               #####
    #####################################################################
    if args.command == "add":
        is_new_space = add_space()

        if is_new_space:
            print("[space-dev] Adding space...")
        else:
            print("[space-dev] Updating space...")

    #####################################################################
    #####                     LOAD SPACE                            #####
    #####################################################################
    elif args.command == "load":
        if args.load:
            space_name = args.load[0]
            load_script = None
            if len(args.load) == 2:
                load_script = args.load[1]
                try:
                    load_script = int(load_script)
                    load_script = parse_load_script_name(load_script)
                except:
                    pass

            # check if the space number was provided
            try:
                space_number = int(space_name)
                space_name = parse_space_name(space_number)
            except:
                pass

            if args.ls:
                list_load_scripts(space_name)
                sys.exit()

            load_space(space_name, load_script=load_script)

            print("[space-dev] Executing space " + str(space_name))
        else:
            if args.ls:
                list_spaces()
            else:
                print("[space-dev] Please specify a space name or number to load.")


    #####################################################################
    #####                       START SPACE                         #####
    #####################################################################
    elif args.command == "start":
        if args.ls:
            list_start_scripts()
        else:
            start_space()

    #####################################################################
    #####                      RUN SCRIPT                           #####
    #####################################################################
    elif args.command == "run":
        if args.ls:
            list_scripts()
        else:
            run_script(get_client_base_folder_name(), run=args.run)

    #####################################################################
    #####                       LIST SPACES                         #####
    #####################################################################
    elif args.command == "ls":
        list_spaces()

    #####################################################################
    #####                     REMOVE SPACE                          #####
    #####################################################################
    elif args.command == "rm":
        remove_space(args.rm[0])

    #####################################################################
    #####                           HELP                            #####
    #####################################################################
    elif args.command == None:
        parser.print_help()
    
    sys.exit()
