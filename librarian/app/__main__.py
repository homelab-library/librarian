#!/usr/bin/env python3
import argparse
import os
import yaml
import logging
import asyncio
from pathlib import Path
from .config import parse_args, Config
from .git import Git
from .renderer import Renderer
from .provision import GithubProvisioner


log = logging.getLogger()


class Main(object):
    async def run(self):
        args = parse_args()
        fn = getattr(self, args.command)
        await fn(args)

    async def init(self, cfg: Config):
        await Git.init()

    async def render(self, cfg: Config):
        Renderer().render_container(cfg.container)

    async def pull(self, cfg: Config):
        await Git.update_containers()

    async def resync(self, cfg: Config):
        await Git.update_containers()
        renderer = Renderer()
        for container in cfg.container_names:
            renderer.render_container(container)

    async def provision(self, cfg: Config):
        container_name = cfg.container
        provisioner = GithubProvisioner(cfg)
        provisioner.provision_repo(container_name)
        await Git.init_container(container_name)
        Renderer().render_container(container_name)
        await Git.commit_new_container(container_name)

    async def push_all(self, cfg: Config):
        await Git.push_containers()


if __name__ == '__main__':
    os.chdir("/workspace")
    asyncio.run(Main().run())
