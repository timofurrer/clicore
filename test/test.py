#!/usr/bin/python

import cli


if __name__ == "__main__":
    my_cli = cli.Cli(".my_cli.history", "Hello everybody")
    my_cli.set_prompt("MyCLI> ")
    my_cli.register_item(cli.CliItem("my_item"))
    my_cli.register_item(cli.CliItem("item", None, None, True, [cli.CliSysPathItem()]))
    my_cli.start()
    my_cli.stop()
