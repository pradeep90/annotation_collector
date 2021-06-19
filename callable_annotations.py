#!/usr/bin/env python3
from typing import Iterable, List, Callable

import libcst as cst
import libcst.codemod as codemod
from libcst import matchers as m
from pathlib import Path
import sys
import argparse
import textwrap


callable_annotation_matcher = m.Annotation(
    m.Subscript(m.Name("Callable")) | m.Name("Callable")
)
arbitrary_parameter_callable_matcher = m.Annotation(m.Name("Callable"))
MAX_ARITY = 5


def annotation_to_string(annotation: cst.Annotation) -> str:
    return (
        cst.Module(
            [cst.SimpleStatementLine([cst.AnnAssign(cst.Name("x"), annotation)])]
        )
        .code.strip()
        .split(": ")[1]
    )


def callables_of_arity(
    callable_annotations: List[cst.Annotation], arity: int
) -> List[cst.Annotation]:
    callable_arity_matcher = m.Annotation(
        m.Subscript(
            m.Name("Callable"),
            slice=[
                m.SubscriptElement(
                    m.Index(m.List(elements=[m.DoNotCare() for _ in range(arity)]))
                ),
                m.ZeroOrMore(),
            ],
        )
    )
    return [
        annotation
        for annotation in callable_annotations
        if m.matches(
            annotation,
            callable_arity_matcher,
        )
    ]


def print_callables(
    message: str, callables: Iterable[cst.Annotation], show_callables: bool
) -> None:
    print(f"{message}: {len(callables)}")
    for annotation in callables:
        if show_callables:
            print(textwrap.indent(annotation_to_string(annotation), " " * 4))


def main(roots: Iterable[Path], *, show_callables: bool) -> None:
    paths = [path for root in roots for path in root.rglob("*.py")]
    callable_annotations = [
        annotation
        for path in paths
        for annotation in m.findall(
            cst.parse_module(Path(path).read_text()),
            callable_annotation_matcher,
        )
    ]

    for arity in range(MAX_ARITY + 1):
        print_callables(
            f"Callables of arity {arity}",
            callables_of_arity(callable_annotations, arity),
            show_callables,
        )

    print_callables(
        f"Callables with arbitrary parameters",
        [
            annotation
            for annotation in callable_annotations
            if m.matches(annotation, arbitrary_parameter_callable_matcher)
        ],
        show_callables,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-callables", action="store_true", default=False)
    parser.add_argument("root", type=Path, nargs="+")
    arguments = parser.parse_args()
    main(arguments.root, show_callables=arguments.show_callables)
