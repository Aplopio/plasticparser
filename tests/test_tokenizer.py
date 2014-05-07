# -*- coding: utf-8 -*-

import unittest
from plasticparser import tokenizer


class TokenizerTestCase(unittest.TestCase):
    def test_should_tokenize_simple_string(self):
        tokens = tokenizer.tokenize('title:abc')
        self.assertEqual(tokens, [['title', ':', 'abc'], []])

    def test_should_tokenize_simple_quoted_string(self):
        tokens = tokenizer.tokenize('title:"abc def"')
        self.assertEqual(tokens, [['title', ':', 'abc def'], []])

    def test_should_tokenize_simple_continious_colon(self):
        tokens = tokenizer.tokenize('title:"abc:def"')
        self.assertEqual(tokens, [['title', ':', 'abc:def'], []])


    def test_should_tokenize_simple_multiple_terms(self):
        tokens = tokenizer.tokenize('title:"abc def" description:def')
        self.assertEqual(tokens, [['title', ':', 'abc def'], ['description', ':', 'def']])


if __name__ == '__main__':
    unittest.main()
