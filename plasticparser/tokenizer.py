# -*- coding: utf-8 -*-

from peak.util.proxies import LazyProxy
from pyparsing import (
    Word, QuotedString, oneOf, CaselessLiteral, White,
    OneOrMore, Optional, alphanums, srange, ZeroOrMore)
from .grammar_parsers import (
    parse_logical_expression, parse_compare_expression, parse_free_text,
    parse_paren_base_logical_expression, join_brackets, join_words,
    parse_facet_compare_expression, parse_one_or_more_facets_expression,
    parse_single_nested_expression, parse_base_nested_expression,
    parse_single_facet_expression, parse_base_facets_expression,
    parse_type_expression, parse_one_or_more_logical_expressions,
    parse_type_logical_facets_expression)

unicode_printables = u''.join(unichr(c) for c in xrange(65536)
                              if not unichr(c).isspace())


def get_word():
    return Word(unicode_printables, excludeChars=[')'])


def get_value():
    word = Word(unicode_printables, excludeChars=[')'])
    quoted_word = QuotedString('"', unquoteResults=False, escChar='\\')
    return quoted_word | word


def get_key():
    return Word(unicode_printables,
                excludeChars=[':', ':>', ':>=', ':<', ':<=', '('])


def get_operator():
    return oneOf(u": :< :> :<= :>= :=")


def get_logical_operator():
    return CaselessLiteral('AND') | CaselessLiteral('OR') | White().suppress()


def get_logical_expression():
    logical_operator = get_logical_operator()
    compare_expression = get_key() + get_operator() + get_value()
    compare_expression.setParseAction(parse_compare_expression)
    base_logical_expression = (compare_expression
                               + logical_operator
                               + compare_expression).setParseAction(
        parse_logical_expression) | compare_expression | Word(
        unicode_printables).setParseAction(parse_free_text)
    logical_expression = ('(' + base_logical_expression + ')').setParseAction(
        parse_paren_base_logical_expression) | base_logical_expression
    return logical_expression


def get_nested_logical_expression():
    operator = get_operator()
    logical_operator = get_logical_operator()
    value = get_value()
    key = get_key()

    paren_value = '(' + OneOrMore(
        logical_operator | value).setParseAction(join_words) + ')'
    paren_value.setParseAction(join_brackets)
    facet_compare_expression = key + operator + paren_value | value
    facet_compare_expression.setParseAction(parse_facet_compare_expression)
    facet_base_logical_expression = (facet_compare_expression
                                     + Optional(logical_operator)).setParseAction(
                                         parse_logical_expression) | value
    facet_logical_expression = ('(' + facet_base_logical_expression
                                + ')').setParseAction(
        parse_paren_base_logical_expression) | facet_base_logical_expression
    return facet_logical_expression


def get_facet_expression():
    facet_logical_expression = get_nested_logical_expression()
    single_facet_expression = Word(
        srange("[a-zA-Z0-9_.]")) +\
        Optional(
            Word('(').suppress() +
            OneOrMore(facet_logical_expression).setParseAction(
                parse_one_or_more_facets_expression) +
            Word(')').suppress())
    single_facet_expression.setParseAction(parse_single_facet_expression)
    base_facets_expression = OneOrMore(single_facet_expression
                                       + Optional(',').suppress())
    base_facets_expression.setParseAction(parse_base_facets_expression)
    facets_expression = Word('facets:').suppress() \
        + Word('[').suppress() \
        + base_facets_expression + Word(']').suppress()
    return facets_expression


def get_nested_expression():
    facet_logical_expression = get_nested_logical_expression()
    single_nested_expression = Word(
        srange("[a-zA-Z0-9_.]")) +\
        Optional(
            Word('(').suppress() +
            OneOrMore(facet_logical_expression).setParseAction(
                parse_one_or_more_facets_expression) +
            Word(')').suppress())
    single_nested_expression.setParseAction(parse_single_nested_expression)
    base_nested_expression = OneOrMore(single_nested_expression
                                       + Optional(',').suppress())
    base_nested_expression.setParseAction(parse_base_nested_expression)
    nested_expression = Word('nested:').suppress()\
        + Word('[').suppress()\
        + base_nested_expression\
        + Word(']').suppress()
    return nested_expression


def _construct_grammar():
    logical_operator = get_logical_operator()
    logical_expression = get_logical_expression()

    facets_expression = get_facet_expression()
    nested_expression = get_nested_expression()

    # The below line describes how the type expression should be.
    type_expression = Word('type')\
        + Word(':').suppress()\
        + Word(alphanums)\
        + Optional(CaselessLiteral('AND')).suppress()
    type_expression.setParseAction(parse_type_expression)

    base_expression = Optional(type_expression)\
        + ZeroOrMore((facets_expression
                      | nested_expression
                      | logical_expression)
                     + Optional(logical_operator)).setParseAction(
            parse_one_or_more_logical_expressions)
    base_expression.setParseAction(parse_type_logical_facets_expression)

    return base_expression


def _sanitize_query(query_string):
    for char in [u'\n', u'\xa0', u'\t']:
        query_string = query_string.replace(char, u' ')
    return query_string.strip()

grammar = LazyProxy(_construct_grammar)


def tokenize(query_string):
    return grammar.parseString(_sanitize_query(query_string),
                               parseAll=True).asList()[0]
