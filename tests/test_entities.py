# -*- coding: utf-8 -*-

import unittest
from plasticparser import entities


class EntitiesTest(unittest.TestCase):
    def test_should_get_terms_from_tokens(self):
        tokens = [['title', ':', 'abc def'], ['description', ':', 'def'], []]
        terms = entities.get_terms(tokens)
        self.assertEqual(len(terms), 2)
        self.assertEqual(terms[0].get_query(), {"term": {"title": "abc def"}})
        self.assertEqual(terms[1].get_query(), {"term": {"description": "def"}})


if __name__ == '__main__':
    unittest.main()
