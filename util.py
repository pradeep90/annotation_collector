#!/usr/bin/env python3
from typing import Iterable, List

import libcst as cst
from pathlib import Path

SHOW_PROGRESS_EVERY = 20


def get_modules(roots: Iterable[Path]) -> List[cst.Module]:
    files = [path for path in roots if path.is_file()]
    directories = [path for path in roots if not path.is_file()]
    paths = files + [
        path
        for directory in directories
        for path in (*directory.rglob("*.py"), *directory.rglob("*.pyi"))
    ]

    modules = []
    for path in paths:
        try:
            modules.append(cst.parse_module(Path(path).read_text()))
        except Exception as exception:
            print(f"Could not parse path {path}: {exception}\n\n")

    return modules
