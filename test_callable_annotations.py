import unittest
import libcst as cst
import libcst.matchers as m
from textwrap import dedent
from typing import List, Optional
from callable_annotations import (
    callable_annotation_matcher,
    callable_annotations,
    arbitrary_parameter_callable_matcher,
    annotation_to_string,
    callback_protocols,
    FunctionWithCallbackParameters,
    class_definition_to_string,
)


def get_callable_annotations(source: str) -> List[str]:
    return [
        annotation_to_string(annotation)
        for annotation in callable_annotations(
            cst.parse_module(source),
        )
    ]


def get_callback_protocols(source: str) -> List[str]:
    return [
        class_definition_to_string(protocol)
        for protocol in callback_protocols(
            cst.parse_module(dedent(source)),
        )
    ]


def get_callback_function_calls(source: str) -> List[str]:
    return [
        str(function_call)
        for function_call in FunctionWithCallbackParameters.functions_with_callback_parameters(
            cst.parse_module(dedent(source)),
        )
    ]


class CallableAnnotationsTest(unittest.TestCase):
    @staticmethod
    def matches(source: str, matcher: m.BaseMatcherNode) -> None:
        module = cst.parse_module(f"f: {source}")
        return m.matches(module.body[0].body[0].annotation, matcher)

    def assert_matches(self, source: str, matcher: m.BaseMatcherNode) -> None:
        self.assertTrue(self.matches(source, matcher))

    def assert_not_matches(self, source: str, matcher: m.BaseMatcherNode) -> None:
        self.assertFalse(self.matches(source, matcher))

    def test_arbitrary_parameter_callable(self) -> None:
        self.assert_not_matches(
            "Callable[[int], str]",
            arbitrary_parameter_callable_matcher,
        )
        self.assert_matches("Callable", arbitrary_parameter_callable_matcher)
        self.assert_matches(
            "Callable[..., None]",
            arbitrary_parameter_callable_matcher,
        )
        self.assert_matches(
            "Callable[P, R]",
            arbitrary_parameter_callable_matcher,
        )

    def test_callable_onnotations(self) -> None:
        self.assertEqual(
            get_callable_annotations(
                "f: Callable[[int], str]",
            ),
            ["Callable[[int], str]"],
        )
        self.assertEqual(
            get_callable_annotations(
                "f: List[Callable[[int], str]]",
            ),
            ["Callable[[int], str]"],
        )
        self.assertEqual(
            get_callable_annotations(
                "f: Union[int, Callable[[int], str]]",
            ),
            ["Callable[[int], str]"],
        )
        self.assertEqual(
            get_callable_annotations(
                "f: int | Callable[[int], str] | bool",
            ),
            ["Callable[[int], str]"],
        )
        self.assertEqual(
            get_callable_annotations(
                "f: int | bool | Callable[[int], str]",
            ),
            ["Callable[[int], str]"],
        )
        self.assertEqual(
            get_callable_annotations(
                "f: int | bool | str | Callable[[int], str] | bool | str",
            ),
            [],
        )
        self.assertEqual(
            get_callable_annotations("f: int"),
            [],
        )
        self.assertEqual(
            get_callable_annotations(
                "f: List[Tuple[Callable[[int], str]]]",
            ),
            ["Callable[[int], str]"],
        )

    def test_limitations(self) -> None:
        self.assertEqual(
            get_callable_annotations(
                "f: Callable[[Callable[[int], str]], bool]",
            ),
            ["Callable[[Callable[[int], str]], bool]"],
        )
        self.assertEqual(
            get_callable_annotations(
                "F = TypeVar('F', bound=Callable[[int], str])",
            ),
            [],
        )
        self.assertEqual(
            get_callable_annotations(
                "MyAlias = Callable[[int], str]",
            ),
            [],
        )

    def test_callback_protocol(self) -> None:
        self.assertEqual(
            get_callback_protocols(
                """
                class Foo(Protocol):
                    def __call__(self, x: int) -> bool: ...
                """
            ),
            ["Foo - def __call__(self, x: int) -> bool: pass"],
        )
        self.assertEqual(
            get_callback_protocols(
                """
                class NotAProtocol:
                    def __call__(self, x: int) -> bool: ...
                """
            ),
            [],
        )


    def test_callback_parameter(self) -> None:
        self.assertEqual(
            get_callback_function_calls(
                """
                def foo(x, func, y):
                    func(x)
                    func(y)
                    func(*args, **kwargs)
                """
            ),
            ["def foo(x, func, y): ... - func(x) - func(y) - func(*args, **kwargs)"],
        )
