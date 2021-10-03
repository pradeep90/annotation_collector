import unittest
import libcst as cst
from textwrap import dedent
from typing import List
from self_annotation import methods_with_self_annotation
from util import statement_to_string


def get_self_annotations(source: str) -> List[str]:
    return [
        statement_to_string(method)
        for method in methods_with_self_annotation(
            cst.parse_module(dedent(source)),
        )
    ]


class SelfAnnotationTest(unittest.TestCase):
    def test_self_annotation(self) -> None:
        self.assertEqual(
            get_self_annotations(
                """
                class Foo:
                    def some_method(self: _T, other: Union[_T, str]) -> bool: ...
                    def some_classmethod(cls: Type[_T], other: int) -> List[_T]: ...
                    def self_not_annotated(self, other: Union[_T, str]) -> bool: ...
                """
            ),
            [
                "def some_method(self: _T, other: Union[_T, str]) -> bool: ...",
                "def some_classmethod(cls: Type[_T], other: int) -> List[_T]: ...",
            ],
        )
        self.assertEqual(
            get_self_annotations(
                """
                class Foo:
                    def some_method(self, other: Union[_T, str]) -> bool: ...
                    def some_method2(cls, other: int) -> List[int]: ...

                def not_a_method(self: _T, other: Union[_T, str]) -> bool: ...
                """
            ),
            [],
        )
