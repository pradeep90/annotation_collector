import unittest
import libcst as cst
from textwrap import dedent
from typing import List
from .generic_annotation import subscripted_annotations, stats_from_annotations_dict
from util import annotation_to_string


def get_subscripted_annotations(source: str, generic_name: str) -> List[str]:
    return [
        annotation_to_string(annotation)
        for annotation in subscripted_annotations(
            cst.parse_module(dedent(source)),
            generic_name,
        )
    ]


class GenericAnnotationTest(unittest.TestCase):
    def test_annotations(self) -> None:
        self.assertEqual(
            get_subscripted_annotations("f: List[int]", "List"),
            ["List[int]"],
        )
        self.assertEqual(
            get_subscripted_annotations("f: List", "List"),
            ["List"],
        )
        self.assertEqual(
            get_subscripted_annotations("f: list[int]", "List"),
            ["list[int]"],
        )
        self.assertEqual(
            get_subscripted_annotations("f: Dict[str, int]", "Dict"),
            ["Dict[str, int]"],
        )
        self.assertEqual(
            get_subscripted_annotations("f: Callable[[str], int]", "Callable"),
            ["Callable[[str], int]"],
        )
        self.assertEqual(
            get_subscripted_annotations("f: List[int]", "Dict"),
            [],
        )

        self.assertEqual(
            get_subscripted_annotations("f: Tuple[List[int]]", "List"),
            ["List[int]"],
        )
        self.assertEqual(
            get_subscripted_annotations(
                "f: Union[int, List[int]]",
                "List",
            ),
            ["List[int]"],
        )
        self.assertEqual(
            get_subscripted_annotations(
                "f: int | List[int] | bool",
                "List",
            ),
            ["List[int]"],
        )
        self.assertEqual(
            get_subscripted_annotations(
                "f: int | bool | List[int]",
                "List",
            ),
            ["List[int]"],
        )
        self.assertEqual(
            get_subscripted_annotations(
                "f: int | bool | str | List[int] | bool | str",
                "List",
            ),
            [],
        )
        self.assertEqual(
            get_subscripted_annotations("f: int", "List"),
            [],
        )
        self.assertEqual(
            get_subscripted_annotations(
                "f: Tuple[Tuple[List[int]]]",
                "List",
            ),
            ["List[int]"],
        )

    def test_limitations(self) -> None:
        self.assertEqual(
            get_subscripted_annotations(
                "f: List[List[int]]",
                "List",
            ),
            ["List[List[int]]"],
        )
        self.assertEqual(
            get_subscripted_annotations("F = TypeVar('F', bound=List[int])", "List"),
            [],
        )
        self.assertEqual(
            get_subscripted_annotations(
                "MyAlias = List[int]",
                "List",
            ),
            [],
        )
