from unittest import TestCase

import mock

from condent import redent


class TestDictRedent(TestCase):
    def setUp(self):
        patch = mock.patch("condent.fits_on_one_line", return_value=False)
        patch.start()
        self.addCleanup(patch.stop)

    def test_it_does_not_correct_a_correct_single_line(self):
        source = 'd = {"foo" : "bar"}'
        self.assertEqual(redent(source), source)

    def test_it_does_not_correct_a_correct_single_line_even_with_breaks(self):
        source = 'd = {"foo" : "bar"}\n\n'
        self.assertEqual(redent(source), source)

    def test_it_does_not_correct_a_correct_line_with_multiple_items(self):
        source = 'd = {"foo" : "bar", "baz" : "quux"}'
        self.assertEqual(redent(source), source)

    def test_it_trims_extra_brace_spaces(self):
        source = 'd = {   "foo" : "bar"  }'
        self.assertEqual(redent(source), 'd = {"foo" : "bar"}')

    def test_it_splits_up_multiple_items_on_a_line(self):
        source = """
d = {
    "foo" : "bar", "baz" : "quux",
}
"""

        self.assertEqual(redent(source), """
d = {
    "foo" : "bar",
    "baz" : "quux",
}
""")

    def test_it_does_not_split_tuple_assignment(self):
        pass

    def test_it_does_not_split_string_literals(self):
        pass

    def test_it_reindents_items(self):
        source = """
d = {
"foo" : "bar",
        "baz" : "quux",
}
"""

        self.assertEqual(redent(source), """
d = {
    "foo" : "bar",
    "baz" : "quux",
}
""")

    def test_it_reindents_more_if_first_line_is_indented(self):
        source = """
        d = {
"foo" : "bar",
        "baz" : "quux",
}
"""

        self.assertEqual(redent(source), """
        d = {
            "foo" : "bar",
            "baz" : "quux",
        }
""")

    def test_it_puts_multiple_line_dict_braces_on_their_own_lines(self):
        source = 'd = {   "foo" : "bar"\n  }'
        self.assertEqual(redent(source), 'd = {\n    "foo" : "bar",\n}')

    def test_it_fixes_spaces_around_single_line_colons(self):
        source = 'd = {"foo": "bar", "baz":"quux"}'
        self.assertEqual(redent(source), 'd = {"foo" : "bar", "baz" : "quux"}')

    def test_it_can_fix_spaces_around_colons_non_symmetrically(self):
        source = 'd = {"foo": "bar", "baz":"quux"}'
        self.assertEqual(
            redent(source, symmetric_colons=False),
            'd = {"foo": "bar", "baz": "quux"}',
        )

    def test_it_fixes_spaces_around_colons(self):
        source = 'd = {"foo": "bar"\n}'
        self.assertEqual(redent(source), 'd = {\n    "foo" : "bar",\n}')

    def test_it_leaves_a_trailing_comma(self):
        source = """
{
    "foo" : "bar",
    "baz" : "quux"
}
"""
        self.assertEqual(redent(source), """
{
    "foo" : "bar",
    "baz" : "quux",
}
""")


class TestOtherDelimiters(TestCase):
    def setUp(self):
        patch = mock.patch("condent.fits_on_one_line", return_value=False)
        patch.start()
        self.addCleanup(patch.stop)

    def test_single_line_function_call(self):
        source = "d = foo(1, 2, 3)"
        self.assertEqual(redent(source), source)

    def test_single_line_set(self):
        source = "d = {1, 2, 3}"
        self.assertEqual(redent(source), source)

    def test_single_line_tuple(self):
        source = "d = (1, 2, 3)"
        self.assertEqual(redent(source), source)

    def test_single_line_list(self):
        source = "d = [1, 2, 3]"
        self.assertEqual(redent(source), source)

    def test_multi_line_function_call(self):
        source = "d = foo(\n1, 2, 3\n)"
        self.assertEqual(redent(source), "d = foo(\n    1,\n    2,\n    3,\n)")

    def test_multi_line_list(self):
        source = """
[1, 2,
3, 4, 5,
6]
"""
        self.assertEqual(redent(source), """
[
    1,
    2,
    3,
    4,
    5,
    6,
]
""")

    def test_if_it_is_confused_it_does_nothing(self):
        source = "awefoijaowf;oiwfe[qpk1240i-"
        self.assertEqual(redent(source), source)


class TestFitsOnOneLine(TestCase):
    def test_it_combines_dicts_that_fit_on_one_line(self):
        source = """
d = {
           "this" : "dict",
"fits" : "on",
      "a single" : "line"
}
"""
        self.assertEqual(
            redent(source),
            '\nd = {"this" : "dict", "fits" : "on", "a single" : "line"}\n')


class TestFullExample(TestCase):
    def setUp(self):
        patch = mock.patch("condent.fits_on_one_line", return_value=False)
        patch.start()
        self.addCleanup(patch.stop)

    def test_full_example(self):
        source = """
            d = {"foo": "bar",
        "baz" : "quux",
                            "spam": "eggs", "cat": "dog",}"""

        self.assertEqual(
            redent(source),
            """
            d = {
                "foo" : "bar",
                "baz" : "quux",
                "spam" : "eggs",
                "cat" : "dog",
            }"""
        )
