#!/usr/bin/env python3
from typing import Iterable, List, Callable

import libcst as cst
import libcst.codemod as codemod
import libcst.matchers as m
from pathlib import Path
import sys
import argparse
import textwrap
import dataclasses

from util import get_modules, expression_to_string


def expression_to_string(expression: cst.BaseExpression) -> str:
    return cst.Module([cst.SimpleStatementLine([cst.Expr(expression)])]).code.strip()


def register_buffer_arguments(module: cst.Module) -> List[cst.BaseExpression]:
    register_buffer_matcher = m.Call(
        func=m.Attribute(
            value=m.Name(
                value="self",
            ),
            attr=m.Name(
                value="register_buffer",
            ),
        ),
        args=[
            m.DoNotCare(),
            m.Arg(
                value=m.SaveMatchedNode(m.DoNotCare(), name="argument"),
            ),
        ],
    )
    return [
        dictionary["argument"]
        for dictionary in m.extractall(
            module,
            register_buffer_matcher,
        )
    ]


def print_register_buffer_arguments(modules: List[cst.Module], verbose: bool) -> None:
    arguments = [
        argument for module in modules for argument in register_buffer_arguments(module)
    ]
    print(f"Register buffer calls: {len(arguments)}")
    if verbose:
        for argument in arguments:
            print(expression_to_string(argument))


def main(roots: Iterable[Path], verbose: bool) -> None:
    modules = get_modules(roots)
    print_register_buffer_arguments(modules, verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", default=False)
    parser.add_argument("root", type=Path, nargs="+")
    arguments = parser.parse_args()
    main(arguments.root, arguments.verbose)
