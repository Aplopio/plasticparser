# -*- coding: utf-8 -*-

from pyparsing import Word, QuotedString, oneOf, CaselessLiteral, White, OneOrMore, Optional, alphanums, \
    srange, ZeroOrMore


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
        if char not in ['(', ')']:
            value = value.replace(char, u'\{}'.format(char))
    return value

def _replace_with_default_op(tokens, i):
    del tokens[i]

def _parse_free_text(tokens):
    return sanitize_free_text(tokens[0])

def _parse_compare_expression(tokens):
    return u"{}{}{}".format(tokens[0], tokens[1], sanitize_value(tokens[2]))


def _parse_facet_compare_expression(tokens):
    return u"{}{}{}".format(tokens[0], tokens[1], sanitize_facet_value(tokens[2]))


def _parse_logical_expression(tokens):
    if ' ' in tokens.asList():
        [_replace_with_default_op(tokens, i) for i, x in enumerate(tokens.asList()) if x.isspace()]
    return u' '.join(tokens.asList())


def _parse_paren_base_logical_expression(tokens):
    return u'{}{}{}'.format(tokens[0], tokens[1], tokens[2])


def default_parse_func(tokens):
    token_list = tokens.asList()
    return_list = []
    for token in token_list:
        if isinstance(token, Facets):
            return_list.append(token)
            token_list.remove(token)
        if isinstance(token, type):
            return_list.append(token)
            token_list.remove(token)
    if ' ' in token_list:
        [_replace_with_default_op(token_list, i) for i, x in enumerate(token_list) if x.isspace()]
    query = Query(' '.join(token_list))
    return_list.append(query)
    return return_list


_parse_one_or_more_logical_expressions = _parse_base_logical_expression = default_parse_func


def _parse_type_expression(tokens):
    return Type({
        "type": {"value": tokens[1]}
    })


def _parse_type_logical_facets_expression(tokens):
    must_list = []
    should_list = []
    must_not_list = []
    facets = {}
    for token in tokens.asList():
        if isinstance(token, Query):
            query = token.get_query()
        if isinstance(token, Facets):
            facets = token.get_query()
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
        },
        "facets": facets
    }
    if query:
        query_dsl["query"]["filtered"]["query"] = {
            "query_string": {
                "query": query,
                "default_operator": "AND"
            }
        }
    return query_dsl


def _parse_single_facet_expression(tokens):
    facet_key = tokens[0]
    filters = {
        facet_key: {}
    }
    field = facet_key
    if "." in facet_key:
        nested_keys = facet_key.split(".")
        nested_field = u".".join(nested_keys[:-1])
        field = nested_keys[-1]
        filters[facet_key]['nested'] = nested_field

    field = "{}_nonngram".format(field)
    filters[facet_key]["terms"] = {"field": field, "size": 20}
    if len(tokens) > 1:
        filters[facet_key]["facet_filter"] = {
            "query": {
                "query_string": {"query": tokens[1],
                                 "default_operator": "AND"}
            }
        }
    return filters


def _parse_base_facets_expression(tokens):
    facets = {}
    for tok in tokens.asList():
        facets.update(tok)
    return Facets(facets)

def join_words(tokens):
    if ' ' in tokens.asList():
        [_replace_with_default_op(tokens, i) for i, x in enumerate(tokens.asList()) if x.isspace()]
    return u' '.join(tokens.asList())


def join_brackets(tokens):
    return u''.join(tokens.asList())

def _parse_one_or_more_facets_expression(tokens):
    return u' '.join(tokens)

def _construct_grammar():
    unicode_printables = u''.join(unichr(c) for c in xrange(65536)
                                  if not unichr(c).isspace())
    word = Word(unicode_printables, excludeChars=[')'])
    quoted_word = QuotedString('"', unquoteResults=False, escChar='\\')
    operator = oneOf(u": :< :> :<= :>= :=")
    logical_operator = CaselessLiteral('AND') | CaselessLiteral('OR') | White()
    value = quoted_word | word
    key = Word(unicode_printables,
               excludeChars=[':', ':>', ':>=', ':<', ':<=', '('])


    paren_value = '(' + OneOrMore(logical_operator | value).setParseAction(join_words) + ')'
    paren_value.setParseAction(join_brackets)
    # The below 4 lines describes logical operators grammar having compare expression or just values
    compare_expression = key + operator + value
    compare_expression.setParseAction(_parse_compare_expression)
    base_logical_expression = (compare_expression + logical_operator + compare_expression).setParseAction(
        _parse_logical_expression) | compare_expression | Word(unicode_printables).setParseAction(_parse_free_text)
    logical_expression = ('(' + base_logical_expression + ')').setParseAction(
        _parse_paren_base_logical_expression) | base_logical_expression

    # The below 4 lines, specific to facets describes logical operators grammar having compare expression or just values
    facet_compare_expression = key + operator + paren_value | value
    facet_compare_expression.setParseAction(_parse_facet_compare_expression)
    facet_base_logical_expression = (facet_compare_expression + Optional(logical_operator)).setParseAction(
        _parse_logical_expression) | value
    facet_logical_expression = ('(' + facet_base_logical_expression + ')').setParseAction(
        _parse_paren_base_logical_expression) | facet_base_logical_expression


    # The below 3 lines describe how a facet expression should be
    single_facet_expression = Word(srange("[a-zA-Z0-9_.]")) + Optional(Word('(').suppress() + OneOrMore(facet_logical_expression).setParseAction(_parse_one_or_more_facets_expression) +
                                                                       Word(')').suppress())
    single_facet_expression.setParseAction(_parse_single_facet_expression)
    base_facets_expression = OneOrMore(single_facet_expression + Optional(',').suppress())
    base_facets_expression.setParseAction(_parse_base_facets_expression)
    facets_expression = Word('facets:').suppress() + Word('[').suppress() + base_facets_expression + Word(']').suppress()

    # The below line describes how the type expression should be.
    type_expression = Word('type') + Word(':').suppress() + Word(alphanums) + Optional(
        CaselessLiteral('AND')).suppress()
    type_expression.setParseAction(_parse_type_expression)

    # The below lines describes the final grammar
    base_expression = Optional(type_expression) +  \
        ZeroOrMore(facets_expression | logical_expression + Optional(logical_operator)).setParseAction(
        _parse_one_or_more_logical_expressions)

    base_expression.setParseAction(_parse_type_logical_facets_expression)

    return base_expression


grammar = _construct_grammar()


def tokenize(query_string):
    return grammar.parseString(query_string.replace('\n', '').strip(),
                               parseAll=True).asList()[0]
