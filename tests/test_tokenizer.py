from plasticparser import tokenizer
from plasticparser.entities import TypeFilter, Query, Expression

import unittest


class TokenizerTest(unittest.TestCase):
    def test_should_sanitize_value(self):
        for char in tokenizer.RESERVED_CHARS:
            sanitized_value = tokenizer.sanitize_value("abc{}".format(char))
            self.assertEqual(sanitized_value, 'abc\\{}'.format(char))

    def test_should_tokenize_and_parse_logical_expression(self):
        query_string = "abc:>def"
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(parsed_string, "abc:>def")

        query_string = "abc:>def and mms:>asd"
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(parsed_string, "abc:>def and mms:>asd")

        query_string = "abc:>def mms:>asd"
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(parsed_string, "abc:>def and mms:>asd")

        query_string = "(abc:>def mms:>asd)"
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(parsed_string, "(abc:>def and mms:>asd)")

        query_string = "abc:>def mms:>asd (abc:def or pqe:123) and blab:blab"
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(parsed_string, "abc:>def and mms:>asd and (abc:def or pqe:123) and blab:blab")

        query_string = "( abc:>def mms:>asd ) (abc:>def mms:>asd) "
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(parsed_string, "(abc:>def and mms:>asd) and (abc:>def and mms:>asd)")

        query_string = "( abc:>def mms:>asd ) and (abc:>def mms:>asd) "
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(parsed_string, "(abc:>def and mms:>asd) and (abc:>def and mms:>asd)")
