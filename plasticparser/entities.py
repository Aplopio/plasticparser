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


class Entity(object):
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Filter(Entity):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_query(self):
        clause = "terms" if isinstance(self.value, list) else "term"
        return {
            clause: {
                self.key: self.value
            }
        }


class TypeFilter(Filter):
    def __init__(self, value):
        Filter.__init__(self, 'type', value)

    def get_query(self):
        return {
            "type": {
                "value": self.value
            }
        }


class Filters(Entity):
    def __init__(self, global_filters_dict=None, type_filter=None):
        global_filters_dict = global_filters_dict if global_filters_dict else {}

        def _construct_filters_(operator):
            if not global_filters_dict:
                return []
            return [Filter(pair.keys()[0], pair[pair.keys()[0]]) for pair in
                    global_filters_dict[('%s' % operator)]] \
                if global_filters_dict.get(operator) else []

        self.must_filters = _construct_filters_('and')
        self.should_filters = _construct_filters_('or')
        self.not_filters = _construct_filters_('not')
        if type_filter:
            self.must_filters.append(type_filter)

    def get_query(self):
        return {
            'bool': {
                'must': [fltr.get_query() for fltr in self.must_filters],
                'should': [fltr.get_query() for fltr in self.should_filters],
                'must_not': [fltr.get_query() for fltr in self.not_filters]
            }
        }


class Query(Entity):
    def __init__(self, query):
        self.query = _escape_input_query(query)

    def get_query(self):
        return {
            "query_string": {
                "query": self.query

            }
        }


class Expression(Entity):
    def __init__(self, type_filter, query, filters=None):
        self.type_filter = type_filter
        self.query = query
        self.filters = filters

    def get_query(self):
        return {
            "query": {
                "filtered": {
                    "query": self.query.get_query(),
                    "filter": self.filters.get_query()
                }
            }
        }

