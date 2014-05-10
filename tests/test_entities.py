# -*- coding: utf-8 -*-

import unittest
from plasticparser import entities
from plasticparser.entities import Filter, Query


class FiltersTest(unittest.TestCase):
    def test_should_get_multiple_filters(self):
        filter_tokens = [['type', ':', 'help'], ['client_id', ':', '1']]
        expected_query = {
            "and": [
                {
                    "type": {"value": "help"}
                },
                {
                    "term": {"client_id": "1"}
                }
            ]
        }

        filters = entities.Filters(filter_tokens)

        self.assertEqual(len(filters.filter_list), 2)
        self.assertEqual(filters.get_query(), expected_query)

    def test_should_get_type_filters(self):
        filter_tokens = [['type', ':', 'help'], ['client_id', ':', '1']]
        expected_query = {
            "type": {
                "value": 'help'
            }
        }

        filters = entities.Filters(filter_tokens)

        self.assertEqual(filters.has_type_filter(), True)
        self.assertEqual(filters.get_type_filters()[0].get_query(), expected_query)

    def test_should_sanitize_special_characters_in_terms(self):
        for char in Filter.RESERVED_CHARS:
            term = Filter(['title', ':', 'abc def' + char])
            self.assertEqual(term.value, "abc def\\" + char)


class QueryTest(unittest.TestCase):
    def test_should_construct_query_from_tokens(self):
        tokens = [['title', ':', 'abc def'], ['description', ':', 'def']]
        expected_query = [
            {
                "match": {"title": "abc def"}
            },
            {
                "match": {"description": "def"}
            }
        ]

        query = Query(tokens)

        self.assertEqual(query.get_query(), expected_query)


if __name__ == '__main__':
    unittest.main()
