#!/usr/bin/env python3
from typing import cast, Iterable, List, Mapping, Optional

import libcst as cst
import libcst.matchers as m
from pathlib import Path
import argparse
import textwrap

from util import get_modules, statement_to_string

function_with_self_annotation_matcher = m.FunctionDef(
    params=m.Parameters(params=[m.Param(annotation=m.Annotation()), m.ZeroOrMore()])
)


def is_method(
    function: cst.FunctionDef,
    scope_mapping: Mapping[cst.CSTNode, Optional[cst.metadata.Scope]],
) -> bool:
    return isinstance(scope_mapping.get(function), cst.metadata.ClassScope)


def is_staticmethod(
    function: cst.FunctionDef,
) -> bool:
    return len(m.findall(function, m.Decorator(decorator=m.Name("staticmethod")))) > 0


def methods_with_self_annotation(module: cst.Module) -> List[cst.CSTNode]:
    wrapper = cst.metadata.MetadataWrapper(module)
    scope_mapping = wrapper.resolve(cst.metadata.ScopeProvider)
    functions_with_self_annotation = m.findall(
        wrapper.module, function_with_self_annotation_matcher
    )
    return [
        function
        for function in functions_with_self_annotation
        if is_method(cast(cst.FunctionDef, function), scope_mapping)
        and not is_staticmethod(cast(cst.FunctionDef, function))
    ]


def print_methods_with_self_annotations(
    modules: List[cst.Module], verbose: bool
) -> None:
    methods = [
        method for module in modules for method in methods_with_self_annotation(module)
    ]
    print(f"Methods with `self` or `cls` annotations: {len(methods)}")
    if verbose:
        for method in methods:
            indented = textwrap.indent(statement_to_string(method), " " * 4)
            print(f"{indented}\n")


def main(roots: Iterable[Path], verbose: bool, show_progress: bool) -> None:
    print_methods_with_self_annotations(
        get_modules(roots, show_progress=show_progress), verbose
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", default=False)
    parser.add_argument("--show-progress", action="store_true", default=False)
    parser.add_argument("root", type=Path, nargs="+")
    arguments = parser.parse_args()
    main(arguments.root, arguments.verbose, arguments.show_progress)
