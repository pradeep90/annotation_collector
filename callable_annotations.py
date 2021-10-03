#!/usr/bin/env python3
from typing import Iterable, List, Callable, Sequence

import libcst as cst
import libcst.codemod as codemod
import libcst.matchers as m
from pathlib import Path
import sys
import argparse
import textwrap
import dataclasses

from util import get_modules, expression_to_string, type_matcher


top_level_callable_annotation_matcher = m.SaveMatchedNode(
    m.Name("Callable"), name="callable"
) | m.SaveMatchedNode(m.Subscript(m.Name("Callable")), name="callable")

callable_annotation_matcher = type_matcher(top_level_callable_annotation_matcher)

arbitrary_parameter_callable_matcher = m.Annotation(
    ~m.Subscript(
        m.Name("Callable"),
        slice=[
            m.SubscriptElement(m.Index(m.List(elements=[m.AtLeastN(n=0)]))),
            m.ZeroOrMore(),
        ],
    )
)

dunder_call_matcher = m.FunctionDef(name=m.Name("__call__"))

callback_protocol_matcher = m.ClassDef(
    bases=[m.ZeroOrMore(), m.Arg(m.Name("Protocol")), m.ZeroOrMore()],
    body=m.IndentedBlock(body=[m.ZeroOrMore(), dunder_call_matcher, m.ZeroOrMore()]),
)
MAX_NUM_PARAMETERS = 5


@dataclasses.dataclass(frozen=True)
class FunctionWithCallbackParameters:
    function: cst.FunctionDef

    @property
    def calls_to_callback_parameters(self) -> List[cst.CSTNode]:
        parameter_names = [
            parameter.name.value for parameter in self.function.params.params
        ]
        return [
            call
            for name in parameter_names
            for call in m.findall(self.function.body, m.Call(func=m.Name(value=name)))
        ]

    @staticmethod
    def functions_with_callback_parameters(
        module: cst.Module,
    ) -> List["FunctionWithCallbackParameters"]:
        functions = []

        try:
            definitions = m.findall(module, m.FunctionDef())
        except Exception as exception:
            print(f"Could not get callback parameters for module due to: {exception}")
            definitions = []

        for function_definition in definitions:
            function = FunctionWithCallbackParameters(function_definition)
            if function.calls_to_callback_parameters:
                functions.append(function)
        return functions

    @staticmethod
    def function_signature_to_string(function: cst.FunctionDef) -> str:
        return cst.Module(
            [
                function.with_changes(
                    body=cst.SimpleStatementSuite([cst.Expr(cst.Ellipsis())]),
                    leading_lines=[],
                    decorators=[],
                )
            ]
        ).code.strip()

    def __str__(self) -> str:
        signature = self.function_signature_to_string(self.function)
        calls = "\n".join(
            expression_to_string(call) for call in self.calls_to_callback_parameters
        )
        return f"""{signature}\n{textwrap.indent(calls, " " * 4)}\n"""


def annotation_to_string(annotation: cst.Annotation) -> str:
    return (
        cst.Module(
            [cst.SimpleStatementLine([cst.AnnAssign(cst.Name("x"), annotation)])]
        )
        .code.strip()
        .split(": ")[1]
    )


def callable_annotations(module: cst.Module) -> List[cst.Annotation]:
    return list(
        cst.Annotation(callable_)
        for dictionary in m.extractall(
            module,
            callable_annotation_matcher,
        )
        for callable_ in dictionary.values()
    )


def callback_protocols(module: cst.Module) -> List[cst.ClassDef]:
    try:
        return list(
            m.findall(
                module,
                callback_protocol_matcher,
            )
        )
    except Exception as exception:
        print(f"Could not get callback protocols for module due to: {exception}")
        return []


def class_definition_to_string(class_: cst.ClassDef) -> str:
    dunder_call_method = m.findall(class_, dunder_call_matcher)[0]
    dunder_call_signature = cst.Module(
        [dunder_call_method.with_changes(body=cst.SimpleStatementSuite([]))]
    ).code.strip()
    return f"{class_.name.value} - {dunder_call_signature}"


def callables_of_arity(
    callable_annotations: List[cst.Annotation], num_parameters: int
) -> List[cst.Annotation]:
    callable_arity_matcher = m.Annotation(
        m.Subscript(
            m.Name("Callable"),
            slice=[
                m.SubscriptElement(
                    m.Index(
                        m.List(elements=[m.DoNotCare() for _ in range(num_parameters)])
                    )
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
    message: str, callables: Sequence[cst.Annotation], show_callables: bool
) -> None:
    print(f"{message}: {len(callables)}")
    if show_callables:
        callable_strings = [annotation_to_string(callable_) for callable_ in callables]
        for string in sorted(callable_strings):
            print(textwrap.indent(string, " " * 4))


def print_callable_data(modules: List[cst.Module], show_callables: bool) -> None:
    annotations = [
        annotation
        for module in modules
        for annotation in callable_annotations(
            module,
        )
    ]

    for num_parameters in range(MAX_NUM_PARAMETERS + 1):
        print_callables(
            f"Callables with {num_parameters} parameters",
            callables_of_arity(annotations, num_parameters),
            show_callables,
        )

    print_callables(
        f"Callables with arbitrary parameters",
        [
            annotation
            for annotation in annotations
            if m.matches(annotation, arbitrary_parameter_callable_matcher)
        ],
        show_callables,
    )


def print_protocol_data(modules: List[cst.Module], show_protocols: bool) -> None:
    protocols = [
        protocol
        for module in modules
        for protocol in callback_protocols(
            module,
        )
    ]

    print(f"Callback Protocols: {len(protocols)}")
    if show_protocols:
        strings = [class_definition_to_string(protocol) for protocol in protocols]
        for string in sorted(strings):
            print(textwrap.indent(string, " " * 4))


def print_functions_with_callback_parameters(
    modules: List[cst.Module], show_progress: bool
) -> None:
    functions = []
    for i, module in enumerate(modules):
        functions_for_module = (
            FunctionWithCallbackParameters.functions_with_callback_parameters(
                module,
            )
        )
        functions.extend(functions_for_module)
        if show_progress:
            print(
                f"Progress: {i}/{len(modules)}."
                f" Current module had {len(functions_for_module)} callbacks."
                f" Total so far: {len(functions)}"
            )

    print(f"Functions with callback parameters: {len(functions)}")
    strings = [str(function) for function in functions]
    for string in sorted(strings):
        print(textwrap.indent(string, " " * 4))


def main(
    roots: Iterable[Path],
    show_callables: bool,
    show_callback_parameters: bool,
    show_progress: bool,
) -> None:
    modules = get_modules(roots, show_progress)

    print_callable_data(modules, show_callables)
    print_protocol_data(modules, show_callables)
    if show_callback_parameters:
        print_functions_with_callback_parameters(modules, show_progress)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-callables", action="store_true", default=False)
    parser.add_argument(
        "--show-callback-parameters", action="store_true", default=False
    )
    parser.add_argument("--show-progress", action="store_true", default=False)
    parser.add_argument("root", type=Path, nargs="+")
    arguments = parser.parse_args()
    main(
        arguments.root,
        arguments.show_callables,
        arguments.show_callback_parameters,
        arguments.show_progress,
    )
