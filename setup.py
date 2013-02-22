# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name="cli",
    description="cli library for python",
    version="0.00.01",
    author="Timo Furrer",
    author_email="tuxtimo@gmail.com",
    url="https://github.com/timofurrer/cli",
    package_dir={"cli.observable": "cli/pyobservable/observable", "cli.colorful": "cli/colorful/colorful"},
    packages=["cli", "cli.observable", "cli.colorful"]
)
