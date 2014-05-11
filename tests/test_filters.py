import unittest
from plasticparser.entities import Filter, Filters, TypeFilter


class FilterTest(unittest.TestCase):
    def test_type_filter_should_get_query(self):
        expected_query = {
            "type": {
                "value": "help"
            }
        }

        query = TypeFilter(['type', ':', 'help']).get_query()

        self.assertEqual(query, expected_query)

    def test_filter_default_get_query(self):
        expected_query = {
            "term": {
                "desc": "help"
            }
        }

        query = Filter(['desc', ':', 'help']).get_query()

        self.assertEqual(query, expected_query)

    def test_should_sanitize_special_characters_in_terms(self):
        for char in Filter.RESERVED_CHARS:
            term = Filter(['title', ':', 'abc def' + char])
            self.assertEqual(term.value, "abc def\\" + char)

    def test_should_not_sanitize_if_value_is_not_string(self):
        term = Filter(['client_id', ':', 1])
        self.assertEqual(term.value, 1)


class FiltersTest(unittest.TestCase):
    def test_should_get_query_for_both_type_and_term_filters(self):
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

        filters = Filters(filter_tokens)
        self.assertEqual(filters.has_type_filters(), True)
        self.assertEqual(filters.has_term_filters(), True)
        self.assertEqual(filters.get_query(), expected_query)

    def test_should_get_only_term_filters(self):
        filter_tokens = [['client_id', ':', '1'], ['user_id', ':', 2]]
        expected_query = {
            "and": [
                {
                    "term": {
                        "client_id": "1"
                    }
                },
                {
                    "term": {
                        "user_id": 2
                    }
                }
            ]
        }

        filters = Filters(filter_tokens)
        query = filters.get_query()

        self.assertEqual(filters.has_type_filters(), False)
        self.assertEqual(filters.has_term_filters(), True)
        self.assertEqual(query, expected_query)

    def test_should_get_query_when_token_list_is_empty(self):
        filter_tokens = []
        expected_query = {}

        filters = Filters(filter_tokens)

        self.assertEqual(filters.has_type_filters(), False)
        self.assertEqual(filters.has_term_filters(), False)
        self.assertEqual(filters.get_query(), expected_query)


if __name__ == '__main__':
    unittest.main()
