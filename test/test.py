#!/usr/bin/python

from clicore.core import Cli, CliItem, CliSysPathItem
from clicore.clihelper import CliHelper


class MyCli(Cli):
    def __init__(self):
        Cli.__init__(self, ".my_cli.history", "Hello everybody")
        self.set_prompt("MyCli> ")

        self.register_item(CliItem("my_item"))
        self.register_item(CliItem("item", None, None, True, [CliSysPathItem()]))
        self.register_item(CliItem("bla", self.bla))
        self.register_item(CliItem("foo", self.foo))
        self.register_item(CliHelper.create_help_item(self))

    @Cli.obs.on("initialized")
    def initialized(self):
        print "on_initialized"

    @Cli.obs.on("before_start")
    def before_start(self):
        print "before_start"

    @Cli.obs.on("before_stop")
    def before_stop(self):
        print "before_stop"

    def bla(self, item, args, line_input):
        """
            arguments: <bla> [--foo]
            description: this command echoes just bla
        """
        print "bla"

    def foo(self, item, args, line_input):
        """some stupid command with wrong help"""
        print "foooo"


if __name__ == "__main__":
    my_cli = MyCli()
    my_cli.start()
