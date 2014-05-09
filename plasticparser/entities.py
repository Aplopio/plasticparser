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
            "match": {
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
    def __init__(self, tokens):
        self.items = [Filter(token) for token in tokens[1] if token]
        if tokens[0]:
            type_filter = TypeFilter(tokens[0])
            self.items.insert(0, type_filter)

    def has_type_filter(self):
        return isinstance(self.items[0], TypeFilter)

    def get_type_filter(self):
        return self.items[0]

    def get_term_filters(self):
        return self.items[1:] if self.has_type_filter() else self.items

