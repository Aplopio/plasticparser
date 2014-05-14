# -*- coding: utf-8 -*-
RESERVED_CHARS = ('\\', '+', '-', '&&',
                  '||', '!', '(', ')',
                  '{', '}', '[', ']',
                  '^', '"', '~', '*',
                  '?', '/', ':')

ESCAPE_CHARS = ('\\', '+', '-', '&&',
                '||', '!',
                '{', '}', '[', ']',
                '^', '"', '~', '*',
                '?', '/')

COMPARISON_OPERATORS = ('>', '<', '<=', '>=')


def _sanitize_term_value(value):
    if not isinstance(value, basestring):
        return value
    for char in RESERVED_CHARS:
        value = value.replace(char, u'\{}'.format(char))
    return value


def _escape_input_query(value):
    if not isinstance(value, basestring):
        return value
    for char in ESCAPE_CHARS:
        value = value.replace(char, u'\{}'.format(char))
    return value


def _translate_operator(operator):
    return ':' + operator if operator in COMPARISON_OPERATORS else operator


class Filter(object):
    def __init__(self, key, value):
        self.key = key
        self.value = _sanitize_term_value(value)

    def get_query(self):
        return {
            "term": {
                self.key: self.value
            }
        }


class TypeFilter(Filter):
    def get_query(self):
        return {
            "type": {
                "value": self.value
            }
        }


class TermFilter(Filter):
    pass


class Filters(object):
    def __init__(self, token_list, type_filters):
        self.token_list = token_list
        self.type_filters = type_filters

    def _get_logical_query(self, logical_type):
        filter_list = []
        if self.token_list:
            filter_list = [Filter(*token.popitem()).get_query() for token in self.token_list.get(logical_type, [])]
        if self.type_filters and logical_type == 'and':
            filter_list.append(TypeFilter(*self.type_filters[0].popitem()).get_query())

        return filter_list

    def get_query(self):
        return {
            'must': self._get_logical_query('and'),
            'should':  self._get_logical_query('or'),
            'must_not': self._get_logical_query('not'),
        }


class MatchClause(object):
    def __init__(self, token_list):
        self.key = token_list[0]
        self.operator = _translate_operator(token_list[1])
        self.value = _sanitize_term_value(token_list[2])

    def get_query(self):
        return "{}{}{}".format(self.key, self.operator, self.value)


def query_string(match_clause):
    return match_clause.get_query()


class Query(object):
    def __init__(self, query):
        self.query = _escape_input_query(query)

    def get_query(self):
        return {
            "query_string": {
                "query": self.query

            }
        }


class Expression(object):
    def __init__(self, query, filters):
        self.filters = filters
        self.query = query

    def get_query(self):
        return {
            "query": {
                "filtered": {
                    "query": self.query.get_query(),
                    "filter":{"bool": self.filters.get_query()}
                }
            }
        }

