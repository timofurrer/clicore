# -*- coding: utf-8 -*-

import os
import readline

from cliitem import CLIItem


class CLI:
    def __init__(self, history_file=None, welcome_text=None, use_location=True):
        # configure readline
        readline.set_completer(self._complete)
        readline.parse_and_bind("tab: complete")

        self._history_file = history_file
        self._welcome_text = welcome_text

        self._started = False
        self._matches = []
        self._items = []

        self._prompt = "CLI> "

    def start(self):
        if self._history_file is not None:
            try:
                readline.read_history_file(os.path.expanduser(self._history_file))
            except IOError:  # occures if history file does not exist yet
                pass

        # TODO: implement hook for "start_before"

        self._started = True
        while self._started:
            try:
                line_input = raw_input(self._prompt)
            except EOFError:  # occures when Ctrl+D is pressed
                # TODO: ask for really existing
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
                print("command cannot be invoked")
        else:
            print("command cannot be found")

    def stop(self):
        # TODO: implement hook for before stop
        if self._history_file is not None:
            readline.write_history_file(self._history_file)
        self._started = False
        # TODO: implement hook for after stop

    def _complete(self, line, state):
        if state == 0:
            self._matches = []
            original_line = readline.get_line_buffer()

            for i in self._items:
                for r in i.complete(original_line):
                    self._matches.append(r)
        m = self._matches[state]
        if isinstance(m, CLIItem):
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

    def register_item(self, item):
        self._items.append(item)

    def clear_items(self):
        for i in self._items:
            self._items.remove(i)

    def remove_item(self, name):
        for i in self._items:
            if i.get_name() == name:
                self._items.remove(i)
