#!/usr/bin/env python3
from pathlib import Path
import yaml
import logging

log = logging.getLogger()


class Data(object):
    @staticmethod
    def merge(left: dict, right: dict, path=[]):
        '''
        Deep merge the right dictionary into the left dictionary.
        This effectively means that the "left" dictionary contains the default values that
        will be overridden by the "right" dictionary.
        '''

        for key in right:
            if key in left:
                if isinstance(left[key], dict) and isinstance(right[key], dict):
                    Data.merge(
                        left[key], right[key], path + [str(key)])
                else:
                    left[key] = right[key]
            else:
                left[key] = right[key]

        return left

    @staticmethod
    def load_file(path: Path):
        result = dict()
        with open(path, "r") as f:
            result = yaml.load(f, Loader=yaml.FullLoader)
        if not result:
            result = dict()
        return result

    @staticmethod
    def load(name: str):
        result = Data.load_file(Path("librarian/defaults.yml"))
        try:
            cfg = Data.load_file(Path("containers") / name / "library.yml")
            Data.merge(result, cfg)
        except Exception as e:
            log.warn("Only using defaults!", e)
        return result
