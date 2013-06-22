# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="clicore",
    description="cli core library for python",
    version="0.00.01",
    author="Timo Furrer",
    author_email="tuxtimo@gmail.com",
    url="https://github.com/timofurrer/cli",
    install_requires=["observable==0.00.03"],
    package_dir={"clicore.colorful": "clicore/colorful/colorful"},
    packages=["clicore", "clicore.colorful"]
)
