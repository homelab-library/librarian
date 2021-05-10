#!/usr/bin/env python3
import logging
import subprocess
import os
import sys
import asyncio
from asyncio import create_subprocess_shell

log = logging.getLogger()
ORG_NAME = "homelab-library"


async def shell(script: str, check=True):
    proc = await create_subprocess_shell(
        script,
        env=os.environ,
    )
    await proc.wait()
    if check and (proc.returncode != 0):
        raise Exception(f"Process failed with RC {proc.returncode}")


class Git(object):
    @staticmethod
    async def init():
        log.info("Initializing submodules")
        await shell("git submodule update --init --remote")
        Git.update_containers()

    @staticmethod
    async def update_containers():
        await shell("""git submodule foreach -q 'branch="$(git config -f $toplevel/.gitmodules submodule.$name.branch)"; git checkout $branch'""")

    @staticmethod
    async def push_containers():
        await shell("""git submodule foreach -q 'git add --all . || true'""")
        await shell("""git submodule foreach -q 'git commit -m "Automated update" || true'""")
        await shell("""git submodule foreach -q 'git push || true'""")

    @staticmethod
    async def init_container(name: str):
        log.info(f"Adding {name} as a submodule")
        newdir = f"containers/{name}"
        await shell(f"git init {newdir}")

    @staticmethod
    async def commit_new_container(name: str):
        message = "Initial commit..."
        log.info(f"Committing and pushing container '{name}'")
        newdir = f"containers/{name}"
        os.chdir(newdir)
        await shell("git add --all .")
        await shell(f"git commit -m '{message}'")
        await shell("git branch -M main")
        await shell(f"git remote add origin git@github.com:{ORG_NAME}/{name}.git", False)
        await shell("git push -u origin main")
        os.chdir("../..")
        await shell(f"git submodule add -b main git@github.com:{ORG_NAME}/{name}.git {newdir}/")
