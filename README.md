# Space Dev #

## Installation ##

Simply copy and paste these lines to your terminal (requires git installed)

```
git clone https://github.com/rodipm/space-dev.git
cd space-dev && ./install.py
```
The 'install.py' file will add the project dir to system PATH and auto install package dependencies.

### Config ###

You must create a file named '.space-dev-config.json' in your desired root space folder.

A sample config file can be

```json
{
    "load": {
        "vscode": [
            "code ."
        ],
        "TMUX": [
            "tmux"
        ]
    },
    "scripts": {
        "git": [
            "rm space_dev && cp space_dev.py space_dev",
            "git add .",
            "git commit -m \"auto commit\"",
            "git push -u origin master"
        ]
    },
    "start": {
        "vscode": [
            "<<ctrl+shift+`>>echo hi",
            "<<ctrl+shift+`>>echo hello"
        ],
        "TMUX": [
            "<<ctrl+b>>",
            "<<ctrl+shift+'>>",
            "<<ctrl+b>>",
            "<<ctrl+shift+%>>"
        ]
    }
}
```

## Usage ##

If 'install.py' was correctly executed and, therefore, the project dir has been added to system`s PATH, one can run space-dev using

> space_dev [-h] {add,load,start,run,ls,rm} ...


no file extension nor path to file required.

```
usage: space_dev [-h] {add,load,start,run,ls,rm} ...

Saves and auto opens your development space

positional arguments:
  {add,load,start,run,ls,rm}

optional arguments:
  -h, --help            show this help message and exit
```

### 1. Add ###
```
usage: space_dev add [-h]

positional arguments:
  add         Add (or updates) a space. Can be used from any space
              subdirectory.

optional arguments:
  -h, --help  show this help message and exit
```

### 2. Load ###
```
usage: space_dev load [-h] [--ls] [load [load ...]]

positional arguments:
  load        Load space

optional arguments:
  -h, --help  show this help message and exit
  --ls        List space's load scripts
```

### 3. Start ###
```
usage: space_dev start [-h] [--ls]

positional arguments:
  start       Start space's application specific scripts

optional arguments:
  -h, --help  show this help message and exit
  --ls        List space's application specific scripts to start
```

### 4. Run ###
```
usage: space_dev run [-h] [--ls] [run]

positional arguments:
  run         Run aditional scripts.

optional arguments:
  -h, --help  show this help message and exit
  --ls        List scripts to run
```

### 5. Rm ###
```
usage: space_dev rm [-h] rm

positional arguments:
  rm          Remove space

optional arguments:
  -h, --help  show this help message and exit
```

### 6. ls ###
```
usage: space_dev ls [-h]

positional arguments:
  ls          List spaces

optional arguments:
  -h, --help  show this help message and exit
```