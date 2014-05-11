# -*- coding: utf-8 -*-

import unittest

from plasticparser.entities import Query


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


if __name__ == '__main__':
    unittest.main()