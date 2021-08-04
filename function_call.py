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


def calls_with_literals(module: cst.Module) -> List[cst.BaseExpression]:
    call_with_literal_matcher = m.Call(
        args=[
            m.ZeroOrMore(),
            m.Arg(
                value=m.SimpleString() | m.Integer() | m.Name("True") | m.Name("False"),
            ),
            m.ZeroOrMore(),
        ],
    )
    return m.findall(
        module,
        call_with_literal_matcher,
    )


def print_register_buffer_arguments(modules: List[cst.Module], verbose: bool) -> None:
    arguments = [
        argument for module in modules for argument in register_buffer_arguments(module)
    ]
    print(f"Register buffer calls: {len(arguments)}")
    if verbose:
        for argument in arguments:
            print(expression_to_string(argument))


def print_calls_with_literals(modules: List[cst.Module], verbose: bool) -> None:
    calls = [call for module in modules for call in calls_with_literals(module)]
    print(f"Calls with literals: {len(calls)}")
    if verbose:
        for call in calls:
            print(expression_to_string(call))


def main(roots: Iterable[Path], verbose: bool) -> None:
    modules = get_modules(roots)
    print_register_buffer_arguments(modules, verbose)
    print("")
    print_calls_with_literals(modules, verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", default=False)
    parser.add_argument("root", type=Path, nargs="+")
    arguments = parser.parse_args()
    main(arguments.root, arguments.verbose)
