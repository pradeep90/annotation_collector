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


def type_subscript_matcher(inner_matcher: m.BaseMatcherNode) -> m.BaseMatcherNode:
    return m.Subscript(
        slice=[
            m.ZeroOrMore(),
            m.SubscriptElement(slice=m.Index(inner_matcher)),
            m.ZeroOrMore(),
        ]
    )


top_level_callable_annotation_matcher = m.SaveMatchedNode(
    m.Name("Callable"), name="callable"
) | m.SaveMatchedNode(m.Subscript(m.Name("Callable")), name="callable")


callable_annotation_matcher = m.Annotation(
    top_level_callable_annotation_matcher
    | type_subscript_matcher(top_level_callable_annotation_matcher)
    | type_subscript_matcher(
        type_subscript_matcher(top_level_callable_annotation_matcher)
    )
)

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
MAX_ARITY = 5


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
    return list(
        m.findall(
            module,
            callback_protocol_matcher,
        )
    )


def class_definition_to_string(class_: cst.ClassDef) -> str:
    dunder_call_method = m.findall(class_, dunder_call_matcher)[0]
    dunder_call_signature = cst.Module(
        [dataclasses.replace(dunder_call_method, body=cst.SimpleStatementSuite([]))]
    ).code.strip()
    return f"{class_.name.value} - {dunder_call_signature}"


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

    for arity in range(MAX_ARITY + 1):
        print_callables(
            f"Callables of arity {arity}",
            callables_of_arity(annotations, arity),
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


def main(roots: Iterable[Path], *, show_callables: bool) -> None:
    files = [path for path in roots if path.is_file()]
    directories = [path for path in roots if not path.is_file()]
    paths = files + [
        path
        for directory in directories
        for path in (*directory.rglob("*.py"), *directory.rglob("*.pyi"))
    ]
    modules = [cst.parse_module(Path(path).read_text()) for path in paths]
    print_callable_data(modules, show_callables)
    print_protocol_data(modules, show_callables)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-callables", action="store_true", default=False)
    parser.add_argument("root", type=Path, nargs="+")
    arguments = parser.parse_args()
    main(arguments.root, show_callables=arguments.show_callables)
