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

    def test_should_return_elastic_search_query_dsl_for_basic_query_with_number_and_underscore_in_field(self):
        query_string = 'type:help due_date:1234456'
        expected_query_dsl = {
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": "due_date:1234456"
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

    def test_should_return_elastic_search_query_dsl_for_queries_with_comparision_operators(self):
        query_string = 'type:help due_date<1234 due_date>1234 due_date<=1234 due_date>=1234'
        expected_query_dsl = {
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": "due_date:<1234 OR due_date:>1234 OR due_date:<=1234 OR due_date:>=1234"
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

        elastic_query_dsl = plasticparser.get_query_dsl(query_string)

        self.assertEqual(elastic_query_dsl, expected_query_dsl)

    def test_should_return_elastic_search_query_dsl_for_basic_query_with_type(self):
        query_string = 'type:help title:hello description:"world"'
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

        elastic_query_dsl = plasticparser.get_query_dsl(query_string)

        self.assertEqual(elastic_query_dsl, expected_query_dsl)

    def test_should_return_elastic_search_query_dsl_for_basic_query_with_global_filters(self):
        query_string = 'type:help title:hello description:"world"'
        global_filters = [{"client_id": 1}, {"user_id": 2}]
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
                                "term": {"client_id": 1}
                            },
                            {
                                "term": {"user_id": 2}
                            },
                            {
                                "type": {"value": "help"}
                            },
                        ]
                    }
                }
            }
        }
        elastic_query_dsl = plasticparser.get_query_dsl(query_string, global_filters)

        self.assertEqual(elastic_query_dsl, expected_query_dsl)


class GetDocTypesTest(unittest.TestCase):
    def test_should_return_doc_types_of_query_string_if_any(self):
        query_string = 'type:help title:hello description:"world"'
        doc_types = plasticparser.get_document_types(query_string)
        self.assertEqual(doc_types, ['help'])


if __name__ == '__main__':
    unittest.main()
