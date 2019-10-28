import argparse

parser = argparse.ArgumentParser(description='Saves and auto opens your development space')

subparsers = parser.add_subparsers(dest="command")
subparsers.required = False

loadparser = subparsers.add_parser("load")
loadparser.add_argument('load', nargs=1, help="Load space", default=None)

lsparser = subparsers.add_parser("ls")
lsparser.add_argument('ls', action="store_true",
                      help="List spaces", default=None)

rmparser = subparsers.add_parser("rm")
rmparser.add_argument('rm', nargs=1, help="Remove space", default=None)

runparser = subparsers.add_parser("run")
runparser.add_argument('run', action="store_true",
                       help="Run aditional scripts.", default=None)

args = parser.parse_args()

print(args)
