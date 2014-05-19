from plasticparser import tokenizer
from plasticparser.entities import TypeFilter, Query, Expression

import unittest


class TokenizerTest(unittest.TestCase):
    def test_should_remove_newline_chars(self):
        query_string = '''
        title:"abc

        def"
        '''
        expected_expression = [Expression(None,
                                          Query('title:"abc        def"'))]

        expression = tokenizer.tokenize(query_string)

        self.assertEqual(expression, expected_expression)

    def test_should_tokenize_simple_string(self):
        expected_expression = [Expression(None,
                                          Query('title:abc'))]

        expression = tokenizer.tokenize('title:abc')

        self.assertEqual(expression, expected_expression)

    def test_should_tokenize_simple_string_with_type(self):
        expected_expression = [Expression(TypeFilter('help'),
                                          Query('title:abc description:xyz'))]

        expression = tokenizer.tokenize('type:help and title:abc description:xyz')

        self.assertEqual(expression, expected_expression)

    def test_should_tokenize_simple_string_with_equality_operators(self):
        expected_expression = [Expression(
            None,
            Query('due_date<1234 valid_until>1234 use_by>=1234 expiry_date<=1234'))]

        expression = tokenizer.tokenize('due_date<1234 valid_until>1234 use_by>=1234 expiry_date<=1234')

        self.assertEqual(expression, expected_expression)

    def test_should_tokenize_simple_quoted_string(self):
        expected_expression = [Expression(None, Query('title:"abc def"'))]

        expression = tokenizer.tokenize('title:"abc def"')

        self.assertEqual(expression, expected_expression)

    def test_should_tokenize_when_field_or_values_contain_undercores(self):
        expected_expression = [Expression(None, Query('due_date:123456'))]

        expression = tokenizer.tokenize('due_date:123456')

        self.assertEqual(expression, expected_expression)

    def test_should_tokenize_simple_continuous_colon(self):
        expected_expression = [Expression(None, Query('title:"abc:def"'))]

        expression = tokenizer.tokenize('title:"abc:def"')

        self.assertEqual(expression, expected_expression)

    def test_should_tokenize_simple_multiple_terms(self):
        expected_expression = [Expression(None, Query('title:"abc def" description:def'))]

        expression = tokenizer.tokenize('title:"abc def" description:def')

        self.assertEqual(expression, expected_expression)


if __name__ == '__main__':
    unittest.main()
