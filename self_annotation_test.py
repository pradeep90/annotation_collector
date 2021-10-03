import unittest
import libcst as cst
from textwrap import dedent
from typing import List
from self_annotation import methods_with_self_annotation, methods_returning_self
from util import statement_to_string


def get_self_annotations(source: str) -> List[str]:
    return [
        statement_to_string(method)
        for method in methods_with_self_annotation(
            cst.parse_module(dedent(source)),
        )
    ]


def get_methods_returning_self(source: str) -> List[str]:
    return [
        statement_to_string(method)
        for method in methods_returning_self(
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

                    @staticmethod
                    def some_method2(x: int) -> List[int]: ...

                def not_a_method(self: _T, other: Union[_T, str]) -> bool: ...
                """
            ),
            [],
        )

    def test_returns_self(self) -> None:
        self.assertEqual(
            get_methods_returning_self(
                """
                class Foo:
                    def some_method(self):
                        self.x = 1
                        return self

                    def some_method2(not_called_self):
                        self.x = 1
                        return not_called_self

                    def some_classmethod(cls, x: int):
                        print("hello")
                        return cls(x)

                    def some_classmethod2(not_called_cls, x: int):
                        print("hello")
                        return not_called_cls(x)

                    def no_return_self(self):
                        return 1

                    def no_parameters():
                        return 1
                """
            ),
            [
                "def some_method(self):\n" "    self.x = 1\n" "    return self",
                "def some_method2(not_called_self):\n"
                "    self.x = 1\n"
                "    return not_called_self",
                "def some_classmethod(cls, x: int):\n"
                '    print("hello")\n'
                "    return cls(x)",
                "def some_classmethod2(not_called_cls, x: int):\n"
                '    print("hello")\n'
                "    return not_called_cls(x)",
            ],
        )
        self.assertEqual(
            get_methods_returning_self(
                """
                def not_a_method(self):
                    return self
                """
            ),
            [],
        )
