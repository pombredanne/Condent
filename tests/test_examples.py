import os
import textwrap
import unittest

from condent import DELIMITERS, Condenter, LiteralBuilder, ParsesDelimiters, tokenize


EXAMPLE_FILE = os.path.join(os.path.dirname(__file__), "examples")
REDENTED_FILE = os.path.join(os.path.dirname(__file__), "redented_examples")
SEP = "---\n"


class Config(object):
    symmetric_colons = True
    trailing_comma = True
    single_line_trailing_comma = False


class TestExamples(unittest.TestCase):
    def test_it_redents_the_examples(self):

        config = Config()
        builder = LiteralBuilder(config)
        delimiters = DELIMITERS.keys() + DELIMITERS.values()
        parser = ParsesDelimiters(delimiters)

        with open(EXAMPLE_FILE) as examples, open(REDENTED_FILE) as expected:
            examples.readline(), expected.readline()  # remove modeline

            examples = [e.splitlines(True) for e in examples.read().split(SEP)]
            expected = [e.splitlines(True) for e in expected.read().split(SEP)]

            for example, expect in zip(examples, expected):
                tokens = (
                    tokenize(parser.parse(line), DELIMITERS, DELIMITERS.values())
                    for line in example
                )

                example = "".join(Condenter(builder, config).redent(tokens))
                expect = "".join(expect)

                try:
                    self.assertEqual(example, expect)
                except Exception:
                    self.dump(example, expect)
                    raise

    def dump(self, example, expected):
        print textwrap.dedent("""

        Example failed:
        ===============

        Got
        ---

        {0}

        Expected
        --------

        {1}

        -----------------------------------------------------------------------

        """).format(example, expected)

