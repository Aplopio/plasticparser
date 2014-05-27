# -*- coding: utf-8 -*-

from pyparsing import Word, QuotedString, oneOf, CaselessLiteral, White, Literal, OneOrMore, Optional, alphanums, alphas, \
    srange

# from .entities import TypeFilter, Query, Expression


# def _got_type_term(tokens):
#     return TypeFilter(tokens[2])


# def _got_query(tokens):
#     return Query(tokens[0])


# def _got_expression(tokens):
#     type_filter = tokens[0] if len(tokens) == 2 else None
#     query = tokens[1] if len(tokens) == 2 else tokens[0]
#     return Expression(type_filter, query)


# def _construct_grammar():
#     unicode_printables = u''.join(unichr(c) for c in xrange(65536))
#     type_term = Literal("type") + ':' + Word(alphas) + Optional(CaselessLiteral('and').suppress())
#     type_term.setParseAction(_got_type_term)
#     query_string = Word(unicode_printables)
#     query_string.setParseAction(_got_query)
#     expression = Optional(type_term) + query_string
#     expression.setParseAction(_got_expression)
#     return expression

RESERVED_CHARS = ('\\', '+', '-', '&&',
                  '||', '!', '(', ')',
                  '{', '}', '[', ']',
                  '^', '"', '~', '*',
                  '?', '/', ':')


def sanitize_value(value):
    if not isinstance(value, basestring):
        return value
    for char in RESERVED_CHARS:
        value = value.replace(char, u'\{}'.format(char))
    return value


def _parse_compare_expression(tokens):
    return u"{}{}{}".format(tokens[0], tokens[1], sanitize_value(tokens[2]))


def _parse_logical_expression(tokens):
    logical_operator = tokens[1]
    if logical_operator.isspace():
        logical_operator = "and"
    return u'{} {} {}'.format(tokens[0], logical_operator, tokens[2])


def _parse_paren_base_logical_expression(tokens):
    return u'{}{}{}'.format(tokens[0], tokens[1], tokens[2])


def _parse_base_logical_expression(tokens):
    if ' ' in tokens.asList():
        and_log_pos = tokens.asList().index(' ')
        tokens[and_log_pos] = 'and'
    return u' '.join(tokens)


def _parse_one_or_more_logical_expressions(tokens):
    if ' ' in tokens.asList():
        and_log_pos = tokens.asList().index(' ')
        tokens[and_log_pos] = 'and'
    return u' '.join(tokens)


def _parse_type_expression(tokens):
    return {
        "type": {"value": tokens[1]}
    }


def _parse_type_logical_facets_expression(tokens):
    must_list = []
    should_list = []
    must_not_list = []
    facets = {}
    if isinstance(tokens[0], dict):
        type_filter = tokens[0]
        if type_filter.keys()[0] == 'type':
            must_list.append(type_filter)
        else:
            facets = tokens[0]
        query = tokens[1]
        if isinstance(tokens[1], dict):
            facets = tokens[1]
            query = tokens[2]
    else:
        query = tokens[0]

    return {
        "query": {
            "filtered": {
                "query": {
                    "query_string": {
                        "query": query
                    }
                },
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



def _parse_single_facet_expression(tokens):
    main_key = tokens[0]
    nested_field = u".".join(main_key.split('.')[:-1])
    return {
        main_key: {
            "terms": {
                "field": main_key[len(main_key) - 1]
            },
            "nested": nested_field,
            "facet_filter": {
                "query": {
                    "query_string": {"query": tokens[1]}
                }
            }
        }
    }


def _parse_base_facets_expression(tokens):
    facets = {}
    for tok in tokens.asList():
        facets.update(tok)
    return facets


def _construct_grammar():
    unicode_printables = u''.join(unichr(c) for c in xrange(65536)
                                  if not unichr(c).isspace())
    word = Word(unicode_printables, excludeChars=[')'])
    quoted_word = QuotedString('"', unquoteResults=False, escChar='\\')
    operator = oneOf(u": :< :> :<= :>= :=")
    logical_operator = CaselessLiteral('and') | CaselessLiteral('or') | White()
    value = quoted_word | word
    key = Word(unicode_printables,
               excludeChars=[':', ':>', ':>=', ':<', ':<='])
    compare_expression = key + operator + value
    compare_expression.setParseAction(_parse_compare_expression)

    base_logical_expression = (compare_expression + logical_operator + compare_expression).setParseAction(
        _parse_logical_expression) | compare_expression

    logical_expression = ('(' + base_logical_expression + ')').setParseAction(
        _parse_paren_base_logical_expression) | base_logical_expression

    type_expression = Word('type') + Word(':').suppress() + Word(alphanums) + Optional(CaselessLiteral('and')).suppress()

    single_facet_expression = Word(srange("[a-zA-Z0-9_.]")) + Word('(').suppress() + logical_expression + Word(')').suppress()
    base_facets_expression = OneOrMore(
        single_facet_expression.setParseAction(_parse_single_facet_expression) + Optional(',').suppress()) + Word(
        ']').suppress()
    facets_expression = Word('facets:').suppress() + Word('[').suppress() + base_facets_expression.setParseAction(_parse_base_facets_expression)

    base_expression = Optional(
        type_expression.setParseAction(_parse_type_expression)) + Optional(facets_expression) + OneOrMore(
        logical_expression + Optional(logical_operator)).setParseAction(
        _parse_one_or_more_logical_expressions)

    base_expression.setParseAction(_parse_type_logical_facets_expression)

    return base_expression


grammar = _construct_grammar()


def tokenize(query_string):
    return grammar.parseString(query_string.replace('\n', '').strip(),
                               parseAll=True).asList()[0]
