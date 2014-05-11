# -*- coding: utf-8 -*-


def _sanitize_term_value(value):
    if not isinstance(value, str):
        return value
    for char in Filter.RESERVED_CHARS:
        value = value.replace(char, u'\{}'.format(char))
    return value


class Filter(object):
    RESERVED_CHARS = ['\\', '+', '-', '&&',
                      '||', '!', '(', ')',
                      '{', '}', '[', ']',
                      '^', '"', '~', '*',
                      '?', ':', '/']

    def __init__(self, tokens):
        self.token = tokens
        self.key = tokens[0]
        self.operator = tokens[1]
        self.value = _sanitize_term_value(tokens[2])

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
    def __init__(self, tokens_list):
        self.filter_list = [TypeFilter(tokens) if tokens[0] == 'type'
                            else TermFilter(tokens)
                            for tokens in tokens_list] if tokens_list else []

    def has_type_filters(self):
        return any(isinstance(filter_element, TypeFilter) for filter_element in self.filter_list)

    def has_term_filters(self):
        return any(isinstance(filter_element, TermFilter) for filter_element in self.filter_list)

    def get_type_filters(self):
        return [filter_element
                for filter_element in self.filter_list
                if isinstance(filter_element, TypeFilter)]

    def get_term_filters(self):
        return [filter_element for filter_element in self.filter_list
                if isinstance(filter_element, TermFilter)]

    def get_query(self):
        if self.filter_list:
            return {
                'and': [filter_element.get_query()
                        for filter_element in self.filter_list]
            }
        return {}


class MatchClause(object):
    def __init__(self, token_list):
        self.key = token_list[0]
        self.operator = token_list[1]
        self.value = token_list[2]

    def get_query(self):
        return "{}{}{}".format(self.key, self.operator, self.value)


def query_string(match_clause):
    return match_clause.get_query()


class Query(object):
    def __init__(self, token_lists):
        self.match_clauses = [MatchClause(token_list) for token_list in token_lists]

    def get_query(self):
        match_queries = map(query_string, self.match_clauses)
        return {
            "query_string": {
                "query": " OR ".join(match_queries)

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
                    "filter": self.filters.get_query()
                }
            }
        }

