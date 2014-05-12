# -*- coding: utf-8 -*-

import unittest
from plasticparser import tokenizer


class TokenizerTestCase(unittest.TestCase):
    def test_should_remove_newline_chars(self):
        query_string = '''
        title:"abc

        def"
        '''
        tokens = tokenizer.tokenize(query_string)
        self.assertEqual(tokens, [[], [['title', ':', 'abc        def']]])

    def test_should_tokenize_simple_string(self):
        tokens = tokenizer.tokenize('title:abc')
        self.assertEqual(tokens, [[], [['title', ':', 'abc']]])

    def test_should_tokenize_simple_string_with_type(self):
        tokens = tokenizer.tokenize('type:help title:abc description:xyz')
        self.assertEqual(tokens, [['type', ':', 'help'], [['title', ':', 'abc'], ['description', ':', 'xyz']]])

    def test_should_tokenize_simple_quoted_string(self):
        tokens = tokenizer.tokenize('title:"abc def"')
        self.assertEqual(tokens, [[], [['title', ':', 'abc def']]])

    def test_should_tokenize_when_field_or_values_contain_undercores(self):
        tokens = tokenizer.tokenize('due_date:123456')
        self.assertEqual(tokens, [[], [['due_date', ':', '123456']]])

    def test_should_tokenize_simple_continious_colon(self):
        tokens = tokenizer.tokenize('title:"abc:def"')
        self.assertEqual(tokens, [[], [['title', ':', 'abc:def']]])

    def test_should_tokenize_simple_multiple_terms(self):
        tokens = tokenizer.tokenize('title:"abc def" description:def')
        self.assertEqual(tokens, [[], [['title', ':', 'abc def'], ['description', ':', 'def']]])





if __name__ == '__main__':
    unittest.main()
