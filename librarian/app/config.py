#!/usr/bin/env python3
import argparse
import os
from pathlib import Path


class Config(object):
    def __init__(self, args):
        self._args = args

    @property
    def container_root(self):
        return Path("containers")

    @property
    def container_names(self):
        result = []
        for i in self.container_root.iterdir():
            if i.is_dir():
                result.append(os.path.basename(f"{i}"))
        return result

    @property
    def command(self):
        return getattr(self._args, 'command')

    @property
    def container(self):
        return getattr(self._args, 'container', None)

    @property
    def github_token(self):
        return os.environ.get("GITHUB_TOKEN", None)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="./librarian.sh"
    )

    subparsers = parser.add_subparsers(
        title="command",
        description="Available commands",
        dest="command",
        required=True,
    )

    subparsers.add_parser("init")
    add_render_args(subparsers.add_parser("render"))
    add_provision_args(subparsers.add_parser("provision"))
    subparsers.add_parser("resync")
    subparsers.add_parser("pull")
    subparsers.add_parser("push_all")

    return Config(parser.parse_args())


def add_render_args(parser):
    parser.add_argument(
        "container",
        help="Target container to render",
    )


def add_provision_args(parser):
    parser.add_argument(
        "container",
        help="Target container to provision",
    )
