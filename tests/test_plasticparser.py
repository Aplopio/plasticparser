# -*- coding: utf-8 -*-

import unittest
from plasticparser import plasticparser


class PlasticParserTestCase(unittest.TestCase):
    def test_should_return_elastic_search_query_dsl_for_basic_query(self):
        query_string = 'title:hello OR description:"world"'
        elastic_query_dsl = plasticparser.get_query_dsl(query_string)
        expected_query_dsl = {
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": 'title:hello OR description:"world"',
                            "default_operator": "and"
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [],
                            "should": [],
                            "must_not": []
                        }
                    },
                }
            },
            "facets": {},
            "sort": []
        }
        self.assertEqual(elastic_query_dsl, expected_query_dsl)


    def test_should_return_elastic_search_query_dsl_for_queries_with_comparision_operators(self):
        query_string = 'type:help and due_date:<1234 due_date:>1234 due_date:>=1234 (due_date:>=1234)'
        expected_query_dsl = {
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": "due_date:<1234 due_date:>1234"
                            " due_date:>=1234 (due_date:>=1234)",
                            "default_operator": "and"
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [
                                {
                                    "type": {"value": "help"}
                                }
                            ],
                            "should": [],
                            "must_not": []
                        }
                    }
                }
            },
            "facets": {},
            "sort": []
        }
        elastic_query_dsl = plasticparser.get_query_dsl(query_string)
        self.assertEqual(elastic_query_dsl, expected_query_dsl)


    def test_should_return_elastic_search_query_dsl_for_basic_query_with_type(self):
        query_string = 'type:help and title:hello description:"world"'
        expected_query_dsl = {
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": 'title:hello description:"world"',
                            "default_operator": "and"
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [
                                {
                                    "type": {"value": "help"}
                                }
                            ],
                            "should": [],
                            "must_not": []
                        }
                    }
                }
            },
            "facets": {},
            "sort": []
        }

        elastic_query_dsl = plasticparser.get_query_dsl(query_string)
        self.assertEqual(elastic_query_dsl, expected_query_dsl)


    def test_should_return_elastic_search_query_dsl_for_when_no_querystring_with_facets(self):
        query_string = 'type:help facets: [ aaa.bb(abc:def) bbb(cc:ddd) ]'
        expected_query_dsl = {
            "query": {
                "filtered": {
                    "filter": {
                        "bool": {
                            "must": [
                                {
                                    "type": {"value": "help"}
                                }
                            ],
                            "should": [],
                            "must_not": []
                        }
                    }
                }
            },
            'facets': {
                'aaa.bb': {
                    'facet_filter': {
                        'query': {
                            'query_string': {
                                'query': u'abc:def',
                                "default_operator": "and"
                            }
                        }
                    },
                    'terms': {
                        'field': 'bb_nonngram',
                        'size': 20
                    },
                    'nested': u'aaa'},
                'bbb': {
                    'facet_filter': {
                        'query': {
                            'query_string': {
                                'query': u'cc:ddd',
                                "default_operator": "and"
                            }
                        }
                    },
                    'terms': {
                        'field': 'bbb_nonngram',
                        'size': 20
                    }
                }
            },
            'sort': []
        }

        elastic_query_dsl = plasticparser.get_query_dsl(query_string)
        self.assertEqual(elastic_query_dsl, expected_query_dsl)

    def test_should_return_elastic_search_query_dsl_for_basic_query_with_global_filters(self):
        self.maxDiff = None
        query_string = 'type:help and title:hello description:"world"'
        global_filters = {
            'and': [{"client_id": 1},
                    {"user_id": 2}],
            'or': [{"assigned_to": ["/api/v1/users/5/"]}],
            'not': [],
            'sort': [{"created_on": "desc"}]
        }
        expected_query_dsl = {
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": 'title:hello description:"world"',
                            "default_operator": "and"
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [
                                {
                                    'type': {'value': 'help'}
                                },
                                {
                                    'term': {'client_id': 1}
                                },
                                {
                                    'term': {'user_id': 2}
                                }
                            ],
                            "should": [
                                {
                                    "term": {"assigned_to": ["/api/v1/users/5/"]}
                                }
                            ],
                            "must_not": []
                        }
                    }
                }
            },
            "facets": {},
            "sort": [{"created_on": "desc"}]
        }
        elastic_query_dsl = plasticparser.get_query_dsl(query_string, global_filters)
        self.assertEqual(elastic_query_dsl, expected_query_dsl)

    def test_should_return_elastic_search_query_dsl_for_basic_query_with_nested_filters(self):
        self.maxDiff = None
        query_string = 'type:help and title:hello description:"world" nested:[metadata_facets(field_value:(no) field_name:(first))]'
        global_filters = {
            'and': [{"client_id": 1},
                    {"user_id": 2}],
            'or': [{"assigned_to": ["/api/v1/users/5/"]}],
            'not': [],
            'sort': [{"created_on": "desc"}]
        }
        expected_query_dsl = {
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": 'title:hello description:"world"',
                            "default_operator": "and"
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [
                                {
                                    'type': {'value': 'help'}
                                },
                                {
                                    "nested": {
                                        "path": "metadata_facets",
                                        "query": {
                                            "query_string": {
                                                "query": "field_value:(no) field_name:(first)",
                                                "default_operator": "and"
                                            }
                                        }
                                    }
                                },
                                {
                                    'term': {'client_id': 1}
                                },
                                {
                                    'term': {'user_id': 2}
                                },
                            ],
                            "should": [
                                {
                                    "term": {"assigned_to": ["/api/v1/users/5/"]}
                                }
                            ],
                            "must_not": []
                        }
                    }
                }
            },
            "facets": {},
            "sort": [{"created_on": "desc"}]
        }
        elastic_query_dsl = plasticparser.get_query_dsl(query_string, global_filters)
        self.assertEqual(elastic_query_dsl, expected_query_dsl)

    def test_should_return_elastic_search_query_dsl_for_nested_queries(self):
        query_string = 'type:help first_name:asdasd AND (candidate_messages.comments.title:(yes i will) OR due_date:(1234))'
        expected_query_dsl = {
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": u"first_name:asdasd AND (candidate_messages.comments.title:(yes i will) OR due_date:(1234 ))",
                            "default_operator": "and"
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [
                                {
                                    "type": {"value": "help"}
                                }
                            ],
                            "should": [],
                            "must_not": []
                        }
                    }
                }
            },
            "facets": {},
            "sort": []
        }
        elastic_query_dsl = plasticparser.get_query_dsl(query_string)
        self.assertEqual(elastic_query_dsl, expected_query_dsl)



class GetDocTypesTest(unittest.TestCase):
    def test_should_return_doc_types_of_query_string_if_any(self):
        query_string = 'type:help and title:hello description:"world"'
        doc_types = plasticparser.get_document_types(query_string)
        self.assertEqual(doc_types, ['help'])

class IsFacetQueryTest(unittest.TestCase):
    def test_should_return_false_bcoz_is_not_facet_query(self):
        query_string = 'type:help and title:hello description:"world"'
        is_facet_query = plasticparser.is_facet_query(query_string)
        self.assertEqual(is_facet_query, False)

    def test_should_return_true_bcoz_is_facet_query(self):
        query_string = 'type:help and title:hello description:"world" facets[abc]'
        is_facet_query = plasticparser.is_facet_query(query_string)
        self.assertEqual(is_facet_query, True)


if __name__ == '__main__':
    unittest.main()
