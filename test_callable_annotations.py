import unittest
import libcst as cst
import libcst.matchers as m
from typing import List, Optional
from callable_annotations import (
    callable_annotation_matcher,
    callable_annotations,
    arbitrary_parameter_callable_matcher,
    annotation_to_string,
)


def get_callable_annotations(source: str) -> List[str]:
    return [
        annotation_to_string(annotation)
        for annotation in callable_annotations(
            cst.parse_module(source),
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
                "f: Callable[[Callable[[int], str]], bool]",
            ),
            ["Callable[[Callable[[int], str]], bool]"],
        )
        self.assertEqual(
            get_callable_annotations(
                "f: Union[int, Callable[[int], str]]",
            ),
            ["Callable[[int], str]"],
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
