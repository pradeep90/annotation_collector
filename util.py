#!/usr/bin/env python3
from typing import Iterable, List

import libcst as cst
import libcst.matchers as m
from pathlib import Path

SHOW_PROGRESS_EVERY = 20


def get_modules(roots: Iterable[Path], show_progress: bool) -> List[cst.Module]:
    files = [path for path in roots if path.is_file()]
    directories = [path for path in roots if not path.is_file()]
    paths = files + [
        path
        for directory in directories
        for path in (*directory.rglob("*.py"), *directory.rglob("*.pyi"))
    ]

    modules = []
    for i, path in enumerate(paths):
        if show_progress and i > 0 and i % SHOW_PROGRESS_EVERY == 0:
            print(f"PROGRESS: Parsed {i}/{len(paths)} files...")
        try:
            modules.append(cst.parse_module(Path(path).read_text()))
        except Exception as exception:
            print(f"Could not parse path {path}: {exception}\n\n")

    return modules


def annotation_to_string(annotation: cst.Annotation) -> str:
    return (
        cst.Module(
            [cst.SimpleStatementLine([cst.AnnAssign(cst.Name("x"), annotation)])]
        )
        .code.strip()
        .split(": ")[1]
    )


def expression_to_string(expression: cst.BaseExpression) -> str:
    return cst.Module([cst.SimpleStatementLine([cst.Expr(expression)])]).code.strip()


def statement_to_string(statement: cst.CSTNode) -> str:
    return cst.Module([statement]).code.strip()


def type_subscript_matcher(inner_matcher: m.BaseMatcherNode) -> m.BaseMatcherNode:
    return (
        m.Subscript(
            slice=[
                m.ZeroOrMore(),
                m.SubscriptElement(slice=m.Index(inner_matcher)),
                m.ZeroOrMore(),
            ]
        )
        | m.BinaryOperation(left=inner_matcher)
        | m.BinaryOperation(right=inner_matcher)
    )


def type_matcher(toplevel_matcher: m.BaseMatcherNode) -> m.BaseMatcherNode:
    """Matches `toplevel_matcher` anywhere - as <type>, List[<type>], List[List[<type>]].

    This currently only goes two levels deep."""

    return m.Annotation(
        toplevel_matcher
        | type_subscript_matcher(toplevel_matcher)
        | type_subscript_matcher(type_subscript_matcher(toplevel_matcher))
    )
