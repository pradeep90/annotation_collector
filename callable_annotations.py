#!/usr/bin/env python3
from typing import *

import libcst as cst
import libcst.codemod as codemod
from libcst import matchers as m
from pathlib import Path
import sys


def annotation_to_string(annotation):
    return (
        cst.Module(
            [cst.SimpleStatementLine([cst.AnnAssign(cst.Name("f"), annotation)])]
        )
        .code.strip()
        .split(": ")[1]
    )

def main(root: Path) -> None:
    paths = root.rglob("*.py")
    callable_annotations = [
        annotation
        for path in paths
        for annotation in m.findall(
            cst.parse_module(Path(path).read_text()),
            m.Annotation(m.Subscript(m.Name("Callable")) | m.Name("Callable")),
        )
    ]
    for annotation in callable_annotations:
        print(annotation_to_string(annotation))


if __name__ == "__main__":
    root = sys.argv[1]
    main(Path(root))
