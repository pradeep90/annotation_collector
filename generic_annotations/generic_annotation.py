#!/usr/bin/env python3
from typing import Dict, Iterable, List, Callable, Sequence

import libcst as cst
import libcst.codemod as codemod
import libcst.matchers as m
from pathlib import Path
import sys
import argparse
import textwrap
import dataclasses

from ..util import get_modules, annotation_to_string, expression_to_string, type_matcher

GENERIC_NAMES = [
    "Union",
    "Callable",
    "Optional",
    "List",
    "Dict",
    "Set",
    "Tuple",
    "Iterable",
]

def subscripted_annotation_matcher(generic_name: str) -> m.BaseMatcherNode:
    top_level_annotation_matcher = (
        m.SaveMatchedNode(m.Name(generic_name), name="annotation")
        | m.SaveMatchedNode(m.Name(generic_name.lower()), name="annotation")
        | m.SaveMatchedNode(m.Subscript(m.Name(generic_name)), name="annotation")
        | m.SaveMatchedNode(
            m.Subscript(m.Name(generic_name.lower())), name="annotation"
        )
    )
    return type_matcher(top_level_annotation_matcher)


def subscripted_annotations(
    module: cst.Module, generic_name: str
) -> List[cst.Annotation]:
    return list(
        # pyre-fixme[6]: Bad libcst type.
        cst.Annotation(annotation)
        for dictionary in m.extractall(
            module,
            subscripted_annotation_matcher(generic_name),
        )
        for annotation in dictionary.values()
    )


def stats_from_annotations_dict(
    annotations_dict: Dict[str, List[cst.Annotation]]
) -> str:
    def name_annotations_to_string(name: str, annotations: List[cst.Annotation]) -> str:
        instances = "\n".join(
            textwrap.indent(annotation_string, " " * 4)
            for annotation_string in sorted(
                annotation_to_string(annotation) for annotation in annotations
            )
        )
        return f"`{name}` annotations: {len(annotations)}\n{instances}"

    return "\n\n".join(
        name_annotations_to_string(name, annotations)
        for name, annotations in annotations_dict.items()
    )


def main(
    roots: Iterable[Path],
    show_progress: bool,
) -> None:
    modules = get_modules(roots, show_progress)
    annotations_dict = {
        name: [
            annotation
            for module in modules
            for annotation in subscripted_annotations(module, name)
        ]
        for name in GENERIC_NAMES
    }
    print(stats_from_annotations_dict(annotations_dict))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-progress", action="store_true", default=False)
    parser.add_argument("root", type=Path, nargs="+")
    arguments = parser.parse_args()
    main(
        arguments.root,
        arguments.show_progress,
    )
