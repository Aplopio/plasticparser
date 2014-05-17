import unittest

from plasticparser.entities import Filters, TypeFilter, Filter, GlobalFilters, BooleanFilter


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
    def test_should_give_final_filter(self):
        token_list = {
            'and': [{'client_id': 1}, {'user_id': 2}],
            'or': [{'ass_id': 22}, {'kass_id': 44}],
            'not': [{'ff_id': 33}]
        }
        type_filters = [TypeFilter('help')]

        filters = Filters(token_list, type_filters)
        query = filters.get_query()
        expected_query = {
            "must": [
                {
                    "term": {
                        "client_id": 1
                    }
                },
                {
                    "term": {
                        "user_id": 2
                    }
                },
                {
                    "type": {
                        "value": u"help"
                    }
                }
            ],
            "should": [
                {
                    "term": {
                        "ass_id": 22
                    }
                },
                {
                    "term": {
                        "kass_id": 44
                    }
                }
            ],
            "must_not": [
                {
                    "term": {
                        "ff_id": 33
                    }
                },
            ]
        }
        self.assertEqual(query, expected_query)


class GlobalFiltersTest(unittest.TestCase):
    def test_should_create_global_filters(self):
        expected_filters = [BooleanFilter('and',
                                          [Filter('client_id', 1), Filter('user_id', 2)]),
                            BooleanFilter('or',
                                          [Filter('assigned_to', ["/api/v1/users/5/"])]),
                            BooleanFilter('not', [])]
        global_filter_dict = {
            'and': [{"client_id": 1},
                    {"user_id": 2}],
            'or': [{"assigned_to": ["/api/v1/users/5/"]}],
            'not': []
        }
        global_filters = GlobalFilters(global_filter_dict)
        filters = global_filters.filters
        self.assertEqual(len(filters), len(expected_filters))
        for fltr in filters:
            self.assertTrue(fltr in expected_filters)


class BooleanFilterTest(unittest.TestCase):
    def test_should_get_query_for_and_filter(self):
        boolean_filter = BooleanFilter('and', [{"client_id": 1}, {"user_id": 2}])

        if __name__ == '__main__':
            unittest.main()
