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
                    "query": {
                        "query_string": {
                            "query": 'title:hello OR description:world'}
                    },
                    "filter": {

                    },
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
                    "query": {
                        "query_string": {
                            "query": "title:hello OR description:world"
                        }
                    },
                    "filter": {
                        "and": [
                            {
                                "type": {"value": "help"}
                            }
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


class GetDocTypesTest(unittest.TestCase):
    def test_should_return_doc_types_of_query_string_if_any(self):
        query_string = 'type:help title:hello description:"world"'
        doc_types = plasticparser.get_document_types(query_string)
        self.assertEqual(doc_types, ['help'])


if __name__ == '__main__':
    unittest.main()
