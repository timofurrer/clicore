#!/usr/bin/python

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cli"))

import cli


if __name__ == "__main__":
    my_cli = cli.CLI(".my_cli.history", "Hello everybody")
    my_cli.set_prompt("MyCLI> ")
    my_cli.register_item(cli.CLIItem("my_item"))
    my_cli.register_item(cli.CLIItem("item", None, None, True, [cli.CLISysPathItem()]))
    my_cli.start()
    my_cli.stop()
