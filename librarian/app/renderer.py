#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pathlib import Path
from .data import Data
import shutil
import os
import logging
import mdformat

log = logging.getLogger()

TEMPLATE_ROOT = "/workspace/librarian/templates"
CONTAINER_ROOT = "/workspace/containers/"


class Renderer(object):
    def __init__(self):
        self.jinja = Environment(
            loader=FileSystemLoader("/"),
            autoescape=select_autoescape(
                default_for_string=False,
                default=False,
            ),
        )

    def render(self, item, *, data: dict):
        if isinstance(item, str):
            return self.jinja.from_string(item).render(data)
        elif isinstance(item, Path):
            template = self.jinja.get_template(f"{item}")
            return template.render(data)
        else:
            raise Exception(f"Cannot render {itemtype}")

    def render_container(self, container: str):
        dat = Data.load(container)
        self._render_container(
            Path(TEMPLATE_ROOT) / "container",
            Path(CONTAINER_ROOT) / container,
            dat
        )

    def _render_container(self, source: Path, destination: Path, data: dict):
        for filename in os.listdir(f"{source}"):
            filename = Path(filename)
            src = source / filename
            dst = destination / filename
            if src.is_file():
                basename = filename
                if basename.suffix == '.j2':
                    log.info("Rendering template: %s", dst)
                    basename = Path(f"{basename}"[:-3])
                    result = self.render(src, data=data)
                    if basename.suffix == ".md":
                        result = mdformat.text(
                            result,
                            extensions={"tables", "gfm", "toc"}
                        )
                    if result and not result.isspace():
                        with open(destination / basename, "w") as f:
                            f.write(result)
                elif basename.suffix == '.1':
                    basename = Path(f"{basename}"[:-2])
                    target = destination / basename
                    if not target.exists():
                        log.info("Copying %s to %s", src, target)
                        shutil.copy(src, target)
                    else:
                        log.info(
                            "Skipping %s since target alreaady exists", target)
                else:
                    log.info("Copying %s to %s", src, dst)
                    shutil.copy(src, dst)
            else:
                dst.mkdir(parents=True, exist_ok=True)
                self._render_container(src, dst, data)
