# -*- coding: utf-8 -*-

import unittest

from plasticparser.entities import Query, RESERVED_CHARS, MatchClause, COMPARISON_OPERATORS


class QueryTest(unittest.TestCase):
    def test_should_construct_query_from_tokens(self):
        tokens = [['title', ':', 'abc def'], ['description', ':', 'def']]
        expected_query = {
            "query_string": {
                "query": "title:abc def OR description:def"
            }
        }

        query = Query(tokens).get_query()

        self.assertEqual(query, expected_query)


class MatchClauseTest(unittest.TestCase):
    def test_should_sanitize_special_characters_in_terms(self):
        for char in RESERVED_CHARS:
            match_clause = MatchClause(['title', ':', 'abc def' + char])
            self.assertEqual(match_clause.value, "abc def\\" + char)

    def test_should_replace_comparision_operators(self):
        for operator in COMPARISON_OPERATORS:
            match_clause = MatchClause(['foo', operator, 'bar'])
            self.assertEqual(match_clause.operator, ':'+operator)



if __name__ == '__main__':
    unittest.main()
