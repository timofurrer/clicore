# -*- coding: utf-8 -*-

import os
import re


class CliItem(object):
    def __init__(self, name, function=None, value=None, enabled=True, subitems=[], tab_delimiter=" ", categories=[]):
        self._name = name
        self._function = function
        self._value = value
        self._enabled = enabled
        self._subitems = subitems
        self._tab_delimiter = tab_delimiter
        self._categories = categories

    def get_name(self):
        return self._name

    def get_completion_name(self):
        return self._name + self._tab_delimiter

    def get_function(self):
        return self._function

    def get_value(self):
        return self._value

    def get_categories(self):
        return self._categories

    def is_enabled(self):
        return self._enabled

    def set_enabled(self, enabled):
        self._enabled = enabled

    def in_category(self, category):
        return category in self._categories

    def get_item_by_line(self, line):
        if line.startswith(self.get_completion_name()):
            item, args = line.split(self._tab_delimiter, 1)
            if not args:
                return self, args
            else:
                for i in self._subitems:
                    subitem, subargs = i.get_item_by_line(args)
                    if subitem is not None:
                        if subitem.get_function() is not None:
                            return subitem, subargs
                        else:
                            return self, args
                return self, args
        elif self._name == line:
            return self, ""
        else:
            return None, line

    def complete(self, line):
        matches = []
        if self._enabled:
            if line.startswith(self.get_completion_name()):
                item, args = line.split(self._tab_delimiter, 1)
                for s in self._subitems:
                    for i in s.complete(args):
                        matches.append(i)
            elif self.get_completion_name().startswith(line):
                matches.append(self)
        return matches

    def register_subitem(self, subitem):
        self._subitems.append(subitem)

    def get_help(self):
        arguments = ""
        description = self._function.__doc__ or "No description available"
        if self._function and self._function.__doc__ is not None:
            help_str = self._function.__doc__
            arguments_match = re.search("(?:arguments|args):(.*)", help_str)
            description_match = re.search("(?:description|desc):(.*)", help_str)

            if arguments_match:
                arguments = arguments_match.groups()[0].strip()
            if description_match:
                description = description_match.groups()[0].strip()

        return {"arguments": arguments, "description": description}


class CliSysPathItem(CliItem):
    def __init__(self):
        CliItem.__init__(self, "path_item")

    def _listdir(self, root):
        matches = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
            matches.append(name)
        return matches

    def _complete_path(self, path):
        matches = []
        if path == "":
            return self._listdir(".")
        dirname, filename_part = os.path.split(path)
        tmp_dirname = dirname if dirname else "."
        matches = [p for p in self._listdir(tmp_dirname) if p.startswith(filename_part)]
        if len(matches) > 1:
            return matches
        if os.path.isdir(os.path.join(dirname, matches[0])):
            return matches
        return [matches[0] + self._tab_delimiter]

    def complete(self, line):
        return self._complete_path(line)
