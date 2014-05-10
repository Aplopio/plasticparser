# -*- coding: utf-8 -*-
class Filter(object):
    RESERVED_CHARS = ['\\', '+', '-', '&&',
                      '||', '!', '(', ')',
                      '{', '}', '[', ']',
                      '^', '"', '~', '*',
                      '?', ':', '/']

    def __init__(self, token):
        self.token = token
        self.key = token[0]
        self.operator = token[1]
        self.value = self._sanitize(token[2])

    def get_query(self):
        return {
            "term": {
                self.key: self.value
            }
        }

    def _sanitize(self, string):
        for char in Filter.RESERVED_CHARS:
            string = string.replace(char, u'\{}'.format(char))
        return string


class TypeFilter(Filter):
    def get_query(self):
        return {
            "type": {
                "value": self.value
            }
        }


class Filters(object):
    def __init__(self, tokens_list):
        self.filter_list = [TypeFilter(tokens) if tokens[0] == 'type'
                            else Filter(tokens)
                            for tokens in tokens_list] if tokens_list else []

    def has_type_filter(self):
        return any(isinstance(filter_element, TypeFilter) for filter_element in self.filter_list)

    def get_type_filters(self):
        return [filter_element
                for filter_element in self.filter_list
                if isinstance(filter_element, TypeFilter)]

    def get_term_filters(self):
        return [filter_element for filter_element in self.filter_list
                if isinstance(filter_element, TypeFilter)]

    def get_query(self):
        if self.filter_list:
            return {
                'and': [filter_element.get_query()
                        for filter_element in self.filter_list]
            }
        return {}


def _construct_filtered_query(self, filters):
    query_dsl = {}
    if filters.has_type_filter():
        query_dsl['and'] = [filters.get_type_filters().get_query()]
    return query_dsl


class MatchClause(object):
    def __init__(self, token_list):
        self.key = token_list[0]
        self.operator = token_list[1]
        self.value = token_list[2]

    def get_query(self):
        return {
            "match": {
                self.key: self.value
            }
        }


class Query(object):
    def __init__(self, token_lists):
        self.match_clauses = [MatchClause(token_list) for token_list in token_lists]

    def get_query(self):
        return [match_clause.get_query() for match_clause in self.match_clauses]

