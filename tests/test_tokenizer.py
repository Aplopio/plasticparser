from plasticparser import tokenizer
from plasticparser.entities import TypeFilter, Query, Expression

import unittest


class TokenizerTest(unittest.TestCase):
    def test_should_sanitize_value(self):
        for char in tokenizer.RESERVED_CHARS:
            sanitized_value = tokenizer.sanitize_value("abc{}".format(char))
            self.assertEqual(sanitized_value, 'abc\\{}'.format(char))

    def get_query_string(self, parsed_dict):
        return parsed_dict['query']['filtered']['query']['query_string']['query']

    def test_should_tokenize_and_parse_logical_expression(self):
        query_string = "abc:>def"
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(self.get_query_string(parsed_string), "abc:>def")

        query_string = "abc:>def and mms:>asd"
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(self.get_query_string(parsed_string), "abc:>def and mms:>asd")

        query_string = "abc:>def mms:>asd"
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(self.get_query_string(parsed_string), "abc:>def and mms:>asd")

        query_string = "(abc:>def mms:>asd)"
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(self.get_query_string(parsed_string), "(abc:>def and mms:>asd)")

        query_string = "abc:>def mms:>asd (abc:def or pqe:123) and blab:blab"
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(self.get_query_string(parsed_string),
                         "abc:>def and mms:>asd and (abc:def or pqe:123) and blab:blab")

        query_string = "( abc:>def mms:>asd ) (abc:>def mms:>asd) "
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(self.get_query_string(parsed_string), "(abc:>def and mms:>asd) and (abc:>def and mms:>asd)")

        query_string = "( abc:>def mms:>asd ) and (abc:>def mms:>asd) "
        parsed_string = tokenizer.tokenize(query_string)
        self.assertEqual(self.get_query_string(parsed_string), "(abc:>def and mms:>asd) and (abc:>def and mms:>asd)")


    def test_should_parse_logical_expression_with_type(self):
        query_string = "type:def facets: [ aaa(abc:def) ] (abc:>def mms:>asd)"
        parsed_string = tokenizer.tokenize(query_string)
        expected_query_string = {'query': {
            'filtered': {'filter': {'bool': {'should': [], 'must_not': [], 'must': [{'type': {'value': 'def'}}]}},
                         'query': {'query_string': {'query': '(abc:>def and mms:>asd)'}}}}, 'facets': {
            'aaa': {'facet_filter': {'query': {'query_string': {'query': u'abc:def'}}}, 'terms': {'field': 'a'},
                    'nested': u''}}}
        self.assertEqual(parsed_string, expected_query_string)

        query_string = "type:def (abc:>def mms:>asd)"
        parsed_string = tokenizer.tokenize(query_string)
        expected_query_string = {'query': {
        'filtered': {'filter': {'bool': {'should': [], 'must_not': [], 'must': [{'type': {'value': 'def'}}]}},
                     'query': {'query_string': {'query': u'(abc:>def and mms:>asd)'}}}}, 'facets': {}}
        self.assertEqual(parsed_string, expected_query_string)

        query_string = "type:def facets: [ aaa.bb(abc:def) bbb(cc:ddd) ] (abc:>def mms:>asd)"
        parsed_string = tokenizer.tokenize(query_string)
        expected_query_string = {'query': {
            'filtered': {'filter': {'bool': {'should': [], 'must_not': [], 'must': [{'type': {'value': 'def'}}]}},
                         'query': {'query_string': {'query': '(abc:>def and mms:>asd)'}}}}, 'facets': {
            'aaa.bb': {'facet_filter': {'query': {'query_string': {'query': u'abc:def'}}}, 'terms': {'field': 'b'},
                       'nested': u'aaa'},
            'bbb': {'facet_filter': {'query': {'query_string': {'query': u'cc:ddd'}}}, 'terms': {'field': 'b'},
                    'nested': u''}}}
        self.assertEqual(parsed_string, expected_query_string)