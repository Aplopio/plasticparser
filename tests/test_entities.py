# -*- coding: utf-8 -*-

import unittest
from plasticparser import entities
from plasticparser.entities import Term


class EntitiesTest(unittest.TestCase):
    def test_should_get_terms_from_tokens(self):
        tokens = [['title', ':', 'abc def'], ['description', ':', 'def'], []]
        terms = entities.get_terms(tokens)
        self.assertEqual(len(terms), 2)
        self.assertEqual(terms[0].get_query(), {"term": {"title": "abc def"}})
        self.assertEqual(terms[1].get_query(), {"term": {"description": "def"}})

    def test_should_sanitize_special_characters_in_terms(self):
        for char in Term.RESERVED_CHARS:
            term = Term(['title', ':', 'abc def' + char])
            self.assertEqual(term.value, "abc def\\" + char)


if __name__ == '__main__':
    unittest.main()
