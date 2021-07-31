import unittest
import libcst as cst
import libcst.matchers as m
from textwrap import dedent
from typing import List, Optional
from function_call import register_buffer_arguments, expression_to_string


def get_register_buffer_arguments(source: str) -> List[str]:
    return [
        expression_to_string(argument)
        for argument in register_buffer_arguments(
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
