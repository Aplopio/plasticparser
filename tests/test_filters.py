import unittest

from plasticparser.entities import TypeFilter, Filter, Filters


class FilterTest(unittest.TestCase):
    def test_type_filter_should_get_query(self):
        expected_query = {
            "type": {
                "value": "help"
            }
        }

        query = TypeFilter('help').get_query()

        self.assertEqual(query, expected_query)

    def test_filter_default_get_query(self):
        expected_query = {
            "term": {
                "desc": "help"
            }
        }

        query = Filter('desc', 'help').get_query()

        self.assertEqual(query, expected_query)

    def test_should_not_sanitize_if_value_is_not_string(self):
        term = Filter('client_id', 1)
        self.assertEqual(term.value, 1)


class FiltersTest(unittest.TestCase):
    def test_should_create_filters_without_type_filter(self):
        expected_must_filters = [Filter('client_id', 1), Filter('user_id', 2)]
        expected_should_filters = [Filter('assigned_to', ['/api/v1/users/5/'])]
        expected_not_filters = []
        expected_query = {
            "bool": {
                "must": [
                    {
                        "term": {"client_id": 1}
                    },
                    {
                        "term": {"user_id": 2}
                    }
                ],
                "should": [
                    {
                        "terms": {"assigned_to": ["/api/v1/users/5/"]}
                    }
                ],
                "must_not": []
            }
        }
        global_filter_dict = {
            'and': [{"client_id": 1},
                    {"user_id": 2}],
            'or': [{"assigned_to": ["/api/v1/users/5/"]}],
            'not': []
        }
        global_filters = Filters(global_filter_dict)
        self.assertEqual(global_filters.must_filters, expected_must_filters)
        self.assertEqual(global_filters.should_filters, expected_should_filters)
        self.assertEqual(global_filters.not_filters, expected_not_filters)
        self.assertEqual(global_filters.get_query(), expected_query)

    def test_should_create_filters_with_type_filter(self):
        expected_must_filters = [Filter('client_id', 1), Filter('user_id', 2), TypeFilter('help')]
        expected_should_filters = [Filter('assigned_to', ['/api/v1/users/5/'])]
        expected_not_filters = []
        expected_query = {
            "bool": {
                "must": [
                    {
                        "term": {"client_id": 1}
                    },
                    {
                        "term": {"user_id": 2}
                    },
                    {
                        "type": {
                            "value": "help"
                        }
                    }
                ],
                "should": [
                    {
                        "terms": {"assigned_to": ["/api/v1/users/5/"]}
                    }
                ],
                "must_not": []
            }
        }
        global_filter_dict = {
            'and': [{"client_id": 1},
                    {"user_id": 2}],
            'or': [{"assigned_to": ["/api/v1/users/5/"]}],
            'not': []
        }
        global_filters = Filters(global_filter_dict, TypeFilter('help'))
        self.assertEqual(global_filters.must_filters, expected_must_filters)
        self.assertEqual(global_filters.should_filters, expected_should_filters)
        self.assertEqual(global_filters.not_filters, expected_not_filters)
        self.assertEqual(global_filters.get_query(), expected_query)

