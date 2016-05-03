# -*- coding: utf-8 -*-
import plasticparser

RESERVED_CHARS = ('\\', '+', '-', '&&',
                  '||', '!', '(', ')',
                  '{', '}', '[', ']',
                  '^', '~', '*',
                  '?', '/', ':')

class Facets(object):
    def __init__(self, facets_dsl):
        self.facets_dsl = facets_dsl

    def get_query(self):
        return self.facets_dsl


class Aggregations(object):
    def __init__(self, facets_dsl):
        self.facets_dsl = facets_dsl

    def get_query(self):
        return self.facets_dsl


class Nested(object):
    def __init__(self, nested_dsl):
        self.nested_dsl = nested_dsl

    def get_query(self):
        return self.nested_dsl


class Type(object):
    def __init__(self, type_dsl):
        self.type_dsl = type_dsl

    def get_query(self):
        return self.type_dsl


class Query(object):
    def __init__(self, query):
        self.query = query

    def get_query(self):
        return self.query.strip()


def sanitize_value(value):
    if not isinstance(value, basestring):
        return value
    for char in RESERVED_CHARS:
        if char not in "(":
            value = value.replace(char, u'\{}'.format(char))
    return value


def sanitize_facet_value(value):
    if not isinstance(value, basestring):
        return value
    for char in RESERVED_CHARS:
        if char not in ['"', '(', ')']:
            value = value.replace(char, u'\{}'.format(char))
    return value


def sanitize_free_text(value):
    if not isinstance(value, basestring):
        return value
    for char in RESERVED_CHARS:
        if char not in ['(', ')', ':']:
            value = value.replace(char, u'\{}'.format(char))
    return value


def parse_free_text(tokens):
    return sanitize_free_text(tokens[0])


def parse_compare_expression(tokens):
    return u"{}{}{}".format(tokens[0], tokens[1], sanitize_value(tokens[2]))


def parse_facet_compare_expression(tokens):
    return u"{}{}{}".format(tokens[0], tokens[1], sanitize_facet_value(tokens[2]))


def parse_logical_expression(tokens):
    return u' '.join(tokens.asList())


def parse_paren_base_logical_expression(tokens):
    return u'{}{}{}'.format(tokens[0], tokens[1], tokens[2])


def default_parse_func(tokens):
    token_list = tokens.asList()
    return_list = []
    for token in token_list:
        if isinstance(token, Nested):
            return_list.append(token)
            token_list.remove(token)
        if isinstance(token, Facets):
            return_list.append(token)
            token_list.remove(token)
        if isinstance(token, Aggregations):
            return_list.append(token)
            token_list.remove(token)
        if isinstance(token, type):
            return_list.append(token)
            token_list.remove(token)
    query = Query(' '.join(token_list))
    return_list.append(query)
    return return_list


parse_one_or_more_logical_expressions = parse_base_logical_expression = default_parse_func


def parse_type_expression(tokens):
    return Type({
        "type": {"value": tokens[1]}
    })


def parse_type_logical_facets_expression(tokens):
    must_list = []
    should_list = []
    must_not_list = []
    facets = {}
    aggs = {}
    for token in tokens.asList():
        if isinstance(token, Nested):
            nested = token.get_query()
            must_list.append(nested)
        if isinstance(token, Query):
            query = token.get_query()
        if isinstance(token, Facets):
            facets = token.get_query()
        if isinstance(token, Aggregations):
            aggs = token.get_query()
        if isinstance(token, Type):
            type = token.get_query()
            must_list.append(type)
    query_dsl = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": must_list,
                        "should": should_list,
                        "must_not": must_not_list
                    }
                }
            }
        }
    }
    if facets:
        query_dsl['facets'] = facets
    if aggs:
        query_dsl['aggregations'] = aggs
    if query:
        query_dsl["query"]["filtered"]["query"] = {
            "query_string": {
                "query": query,
                "default_operator": getattr(
                    plasticparser, 'DEFAULT_OPERATOR', 'and')
            }
        }
    return query_dsl


def parse_single_facet_expression(tokens):
    facet_key = tokens[0]
    filters = {
        facet_key: {}
    }
    field = facet_key
    if "." in facet_key:
        nested_keys = facet_key.split(".")
        nested_field = u".".join(nested_keys[:-1])

    field = "{}_nonngram".format(field)
    filters[facet_key]["terms"] = {"field": field, "size": getattr(
        plasticparser, 'FACETS_QUERY_SIZE', 20)}
    if len(tokens) > 1:
        filters[facet_key]["facet_filter"] = {
            "query": {
                "query_string": {"query": tokens[1], "default_operator": "and"}
            }
        }

    if len(tokens) > 1 and "." in facet_key:
        filters[facet_key]['nested'] = nested_field
    return filters


def parse_single_aggs_expression(tokens):
    """
    Parses single aggregation query. Following is example input and output:

    INPUT
    type:candidates (name:"John Doe" starred:true) (python or java) facets:[location]

    OUTPUT
    {
        ...
        "aggregations": {
            "location": {
                "aggregations": {
                    "location": {
                        "terms": {
                            "field": "location_nonngram",
                            "size": 20
                        }
                    }
                }
            }
        }
        ...
    }
    """
    aggs_key = tokens[0]
    filters = {
        aggs_key: {
            "aggregations": {
                aggs_key: {}
            }
        }
    }
    field = aggs_key
    if "." in aggs_key:
        nested_keys = aggs_key.split(".")
        nested_field = u".".join(nested_keys[:-1])

    field = "{}_nonngram".format(field)
    filters[aggs_key]["aggregations"][aggs_key]["terms"] = {
        "field": field, "size": getattr(
            plasticparser, 'FACETS_QUERY_SIZE', 20)
    }

    if len(tokens) > 1:
        filters[aggs_key]["aggregations"][aggs_key]["aggregations"] = {
            aggs_key: {'filter': {
                "query": {
                    "query_string": {
                        "query": tokens[1], "default_operator": "and"
                    }
                }
            }}
        }

    if len(tokens) > 1 and "." in aggs_key:
        filters[aggs_key]['nested'] = {'path': nested_field}
    return filters


def parse_base_facets_expression(tokens):
    facets = {}
    for tok in tokens.asList():
        facets.update(tok)
    return Facets(facets)


def parse_base_aggs_expression(tokens):
    aggs = {}
    for tok in tokens.asList():
        aggs.update(tok)
    return Aggregations(aggs)


def join_words(tokens):
    return u' '.join(tokens.asList())


def join_brackets(tokens):
    return u''.join(tokens.asList())


def parse_one_or_more_facets_expression(tokens):
    return u' '.join(tokens)


def parse_one_or_more_aggs_expression(tokens):
    return u' '.join(tokens)


def parse_base_nested_expression(tokens):
    return tokens[0]


def parse_single_nested_expression(tokens):
    return Nested({
        "nested": {
            "path": tokens[0],
            "query": {
                "query_string": {
                    "query": tokens[1],
                    "default_operator": "and"
                }
            }
        }
    })
