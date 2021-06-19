import unittest
import libcst as cst
import libcst.matchers as m
import callable_annotations


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
            callable_annotations.arbitrary_parameter_callable_matcher,
        )
        self.assert_matches(
            "Callable", callable_annotations.arbitrary_parameter_callable_matcher
        )
        self.assert_matches(
            "Callable[..., None]",
            callable_annotations.arbitrary_parameter_callable_matcher,
        )
