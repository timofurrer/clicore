# -*- coding: utf-8 -*-

import os
import readline
from observable import Observable
from colorful import Colorful

from clicore.cliitem import CliItem, CliSysPathItem


class Cli(object):
    obs = Observable()

    def __init__(self, history_file=None, welcome_text=None, use_location=True):
        # configure readline
        readline.set_completer(self._complete)
        readline.parse_and_bind("tab: complete")

        self._history_file = history_file
        self._welcome_text = welcome_text

        self._started = False
        self._matches = []
        self._items = []

        self._prompt = "Cli> "

        # register observable events
        self.obs.register_event("initialized")  # triggered after Cli.__init__
        self.obs.register_event("before_start")  # triggered before cli loop is started
        self.obs.register_event("raw_input_entered")  # triggered after an input is entered
        self.obs.register_event("before_stop")  # triggered before cli loop is stopped
        self.obs.register_event("after_stop")  # triggered after cli loop is stopped

        # trigger 'on.initialized' event
        self.obs.trigger("initialized", self)

    def start(self):
        if self._history_file is not None:
            try:
                readline.read_history_file(os.path.expanduser(self._history_file))
            except IOError:  # occures if history file does not exist yet
                pass

        # trigger 'on.before_start' event
        self.obs.trigger("before_start", self)

        if self._welcome_text:
            print(self._welcome_text)

        self._started = True
        while self._started:
            try:
                line_input = raw_input(self._prompt)
                # trigger 'on.raw_input_entered' event
                self.obs.trigger("raw_input_entered", self)
                if not line_input:
                    continue
            except EOFError:  # occures when Ctrl+D is pressed
                answer = raw_input("\nDo you really want to exit ([y]/n)? ")
                if answer not in ["y", ""]:
                    continue
                self.stop()
                return
            except KeyboardInterrupt:  # occures when Ctrl+C is pressed
                self.stop()
                return

            item, args = self._get_item_by_line(line_input)
            if item is not None:
                f = item.get_function()
                if f is not None:
                    f(item, args, line_input)
                else:
                    Colorful.out.bold_red("command cannot be invoked")
            else:
                Colorful.out.bold_red("command cannot be found")

    def stop(self):
        # trigger 'on.before_stop' event
        self.obs.trigger("before_stop", self)
        if self._history_file is not None:
            readline.write_history_file(self._history_file)
        self._started = False
        # trigger 'on.after_stop' event
        self.obs.trigger("after_stop", self)

    def _complete(self, line, state):
        if state == 0:
            self._matches = []
            original_line = readline.get_line_buffer()

            for i in self._items:
                for r in i.complete(original_line):
                    self._matches.append(r)
        m = self._matches[state]
        if isinstance(m, CliItem):
            return m.get_completion_name()
        return m

    def _get_item_by_line(self, line):
        for i in self._items:
            item, args = i.get_item_by_line(line)
            if item is not None and item.is_enabled():
                return item, args
        return None, line

    def set_prompt(self, prompt):
        self._prompt = prompt

    def set_welcome_text(self, welcome_text):
        self._welcome_text = welcome_text

    def register_item(self, item):
        self._items.append(item)

    def clear_items(self):
        for i in self._items:
            self._items.remove(i)

    def remove_item(self, name):
        for i in self._items:
            if i.get_name() == name:
                self._items.remove(i)

    def enable_items_by_category(self, category):
        for i in self._items:
            i.set_enabled(i.in_category(category))
