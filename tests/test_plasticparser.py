# -*- coding: utf-8 -*-

import unittest
from plasticparser import plasticparser


class PlasticParserTestCase(unittest.TestCase):
    def test_should_return_elastic_search_query_dsl_for_basic_query(self):
        query_string = 'title:hello description:"world"'
        elastic_query_dsl = plasticparser.get_query_dsl(query_string)
        expected_query_dsl = {
            "query": {
                "filtered": {
                    "filter": {
                        "or": [
                            {
                                "term": {"title": "hello"}
                            },
                            {
                                "term": {"description": "world"}
                            },
                        ]
                    }
                }
            }
        }
        self.assertEqual(elastic_query_dsl, expected_query_dsl)

    def test_should_return_elastic_search_query_dsl_for_basic_query_with_type(self):
        query_string = 'type:help title:hello description:"world"'
        elastic_query_dsl = plasticparser.get_query_dsl(query_string)
        expected_query_dsl = {
            "query": {
                "filtered": {
                    "filter": {
                        "and": [
                            {
                                "type": {"value": "help"}
                            }
                        ],
                        "or": [
                            {
                                "term": {"title": "hello"}
                            },
                            {
                                "term": {"description": "world"}
                            },
                        ]
                    }
                }
            }
        }
        self.assertEqual(elastic_query_dsl, expected_query_dsl)



        # def test_should_return_elastic_search_query_dsl_for_simple_search(self):
        #     query_string = 'title:hello AND description:world'
        #     elastic_query_dsl = get_query_dsl(query_string)
        #     expected_query_dsl = {
        #         "query": {
        #             "filtered": {
        #                 "filter": {
        #                     "and": [
        #                         {
        #                             "term": {"title": "hello"}
        #                         },
        #                         {
        #                             "term": {"description": "world"}
        #                         }
        #                     ]
        #                 }
        #             }
        #         }
        #     }
        #     self.assertEqual(elastic_query_dsl, expected_query_dsl)
        #
        #
        # def test_should_return_elastic_search_query_dsl_for_simple_and_or_search(self):
        #     query_string = 'title:hello AND description:world OR title:abc'
        #     elastic_query_dsl = get_query_dsl(query_string)
        #     expected_query_dsl = {
        #         "query": {
        #             "filtered": {
        #                 "filter": {
        #                     "and": [
        #                         {
        #                             "term": {"title": "hello"}
        #                         },
        #                         {
        #                             "term": {"description": "world"}
        #                         }
        #                     ],
        #                     "or": {
        #                             "term": {"title": "abc"}
        #                     }
        #                 }
        #             }
        #         }
        #     }
        #     self.assertEqual(elastic_query_dsl, expected_query_dsl)


if __name__ == '__main__':
    unittest.main()
