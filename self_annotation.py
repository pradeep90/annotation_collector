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


def function_returning_self_matcher(self_parameter_name: str) -> m.BaseMatcherNode:
    return m.FunctionDef(
        body=m.IndentedBlock(
            body=[
                m.ZeroOrMore(),
                m.SimpleStatementLine(
                    body=[
                        m.Return(
                            m.Name(self_parameter_name)
                            | m.Call(m.Name(self_parameter_name))
                        )
                    ]
                ),
            ]
        )
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


def methods_returning_self(module: cst.Module) -> List[cst.CSTNode]:
    wrapper = cst.metadata.MetadataWrapper(module)
    scope_mapping = wrapper.resolve(cst.metadata.ScopeProvider)

    try:
        definitions = m.findall(wrapper.module, m.FunctionDef())
    except Exception as exception:
        print(
            f"Could not get methods returning self or cls for module due to: {exception}"
        )
        definitions = []

    functions = []

    for function in definitions:
        parameters = cast(cst.FunctionDef, function).params.params
        if len(parameters) == 0:
            continue

        first_parameter = parameters[0].name.value
        returns_self = (
            len(m.findall(function, function_returning_self_matcher(first_parameter)))
            > 0
        )
        if is_method(cast(cst.FunctionDef, function), scope_mapping) and returns_self:
            functions.append(function)

    return functions


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
