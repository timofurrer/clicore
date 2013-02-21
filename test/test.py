#!/usr/bin/python

from cli.core import Cli, CliItem, CliSysPathItem


if __name__ == "__main__":
    my_cli = Cli(".my_cli.history", "Hello everybody")
    my_cli.set_prompt("MyCLI> ")
    my_cli.register_item(CliItem("my_item"))
    my_cli.register_item(CliItem("item", None, None, True, [CliSysPathItem()]))
    my_cli.start()
    my_cli.stop()
