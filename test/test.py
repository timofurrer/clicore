#!/usr/bin/python

from clicore.core import Cli, CliItem, CliSysPathItem


class MyCli(Cli):
    def __init__(self):
        Cli.__init__(self, ".my_cli.history", "Hello everybody")
        self.set_prompt("MyCli> ")

        self.register_item(CliItem("my_item"))
        self.register_item(CliItem("item", None, None, True, [CliSysPathItem()]))

    @Cli.obs.on("initialized")
    def initialized(self):
        print "on_initialized"

    @Cli.obs.on("before_start")
    def before_start(self):
        print "before_start"

    @Cli.obs.on("before_stop")
    def before_stop(self):
        print "before_stop"


if __name__ == "__main__":
    my_cli = MyCli()
    my_cli.start()
