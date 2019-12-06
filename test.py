import re
import os

p = re.compile("PATH=\"(.+)\"")

current_dir = os.getcwd()

old_env = open("/etc/environment", "r").read()

if current_dir in old_env:
    print("Diretorio ja esta no PATH!")

try:
    old_path = p.findall(old_env)[0]
    new_env = old_env.replace("PATH=\"" + old_path + "\"", '')
except IndexError:
    old_path = ""
    new_env = old_env


new_path = old_path + ":" + current_dir
new_env = "PATH=\"" + new_path + "\"" + new_env


with open("/etc/environment", "w") as env:
    env.write(new_env)