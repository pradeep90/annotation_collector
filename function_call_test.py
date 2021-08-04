import unittest
import libcst as cst
import libcst.matchers as m
from textwrap import dedent
from typing import List, Optional
from function_call import register_buffer_arguments, calls_with_literals
from util import expression_to_string


def get_register_buffer_arguments(source: str) -> List[str]:
    return [
        expression_to_string(argument)
        for argument in register_buffer_arguments(
            cst.parse_module(dedent(source)),
        )
    ]


def get_calls_with_literals(source: str) -> List[str]:
    return [
        expression_to_string(call)
        for call in calls_with_literals(
            cst.parse_module(dedent(source)),
        )
    ]


class FunctionCallTest(unittest.TestCase):
    def test_register_buffer_arguments(self) -> None:
        self.assertEqual(
            get_register_buffer_arguments(
                """
                class Foo:
                    def __init__(self):
                        self.register_buffer("bar", torch.zeros(10, 20))
                        self.register_buffer("baz", torch.zeros(30, 40))
                """
            ),
            ["torch.zeros(10, 20)", "torch.zeros(30, 40)"],
        )
        self.assertEqual(
            get_register_buffer_arguments(
                """
                class Foo:
                    def __init__(self):
                        self.register_buffer("bar")
                """
            ),
            [],
        )

    def test_calls_with_literals(self) -> None:
        self.assertEqual(
            get_calls_with_literals(
                """
                def foo():
                    bar("hello")
                    baz(x, y, "hello", z)
                """
            ),
            ["""bar("hello")""", """baz(x, y, "hello", z)"""],
        )
        self.assertEqual(
            get_calls_with_literals(
                """
                def foo():
                    bar()
                    baz(x, y)
                """
            ),
            [],
        )
