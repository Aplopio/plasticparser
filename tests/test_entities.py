# -*- coding: utf-8 -*-

import unittest
from plasticparser import entities
from plasticparser.entities import Filter


class EntitiesTest(unittest.TestCase):
    def test_should_get_terms_from_tokens(self):
        tokens = [[],[['title', ':', 'abc def'], ['description', ':', 'def']]]
        filters = entities.Filters(tokens)
        self.assertEqual(len(filters.items), 2)
        self.assertEqual(filters.items[0].get_query(), {"term": {"title": "abc def"}})
        self.assertEqual(filters.items[1].get_query(), {"term": {"description": "def"}})

    def test_should_sanitize_special_characters_in_terms(self):
        for char in Filter.RESERVED_CHARS:
            term = Filter(['title', ':', 'abc def' + char])
            self.assertEqual(term.value, "abc def\\" + char)


    def test_should_get_types_and_terms_from_tokens(self):
        tokens = [['type',':','help'],[['title', ':', 'abc def'], ['description', ':', 'def']]]
        filters = entities.Filters(tokens)
        self.assertEqual(len(filters.items), 3)
        self.assertEqual(filters.items[0].get_query(), {"type": {"value": "help"}})
        self.assertEqual(filters.items[1].get_query(), {"term": {"title": "abc def"}})
        self.assertEqual(filters.items[2].get_query(), {"term": {"description": "def"}})


if __name__ == '__main__':
    unittest.main()
