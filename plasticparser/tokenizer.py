# -*- coding: utf-8 -*-

from pyparsing import Word, Literal, alphas, Optional, CaselessLiteral

from .entities import TypeFilter, Query, Expression


def _got_type_term(tokens):
    return TypeFilter(tokens[2])


def _got_query(tokens):
    return Query(tokens[0])


def _got_expression(tokens):
    type_filter = tokens[0] if len(tokens) == 2 else None
    query = tokens[1] if len(tokens) == 2 else tokens[0]
    return Expression(type_filter, query)


def _construct_grammar():
    unicode_printables = u''.join(unichr(c) for c in xrange(65536))
    type_term = Literal("type") + ':' + Word(alphas) + Optional(CaselessLiteral('and').suppress())
    type_term.setParseAction(_got_type_term)
    query_string = Word(unicode_printables)
    query_string.setParseAction(_got_query)
    expression = Optional(type_term) + query_string
    expression.setParseAction(_got_expression)
    return expression


grammar = _construct_grammar()


def tokenize(string):
    return grammar.parseString(string.replace('\n', '').strip(),
                               parseAll=True).asList()