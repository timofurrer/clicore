#!/usr/bin/python

from clicore.core import Cli, CliItem, CliSysPathItem
from clicore.clihelper import CliHelper


class MyCli(Cli):
    def __init__(self):
        Cli.__init__(self, ".my_cli.history", "Hello everybody")
        self.set_prompt("MyCli> ")

        self.register_item(CliItem("my_item", categories=["basic"]))
        self.register_item(CliItem("item", None, None, True, [CliSysPathItem()]))
        self.register_item(CliItem("bla", self.bla, categories=["basic", "ext"]))
        self.register_item(CliItem("foo", self.foo, categories=["ext"]))
        self.register_item(CliItem("args", self.args, categories=["basic"]))
        self.register_item(CliHelper.create_help_item(self))

        self.enable_category("basic")
        self.disable_category("ext")

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

    def args(self, item, args, line_input):
        """
            arguments: [args...]
            description: print it's arguments
        """
        print args


if __name__ == "__main__":
    my_cli = MyCli()
    my_cli.start()
