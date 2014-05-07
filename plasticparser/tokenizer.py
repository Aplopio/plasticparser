# -*- coding: utf-8 -*-

from pyparsing import Word, Literal, alphas, QuotedString, Group, ZeroOrMore, Optional, OneOrMore


def get_grammar():
    word = Word(alphas)
    exact = QuotedString('"', unquoteResults=True, escChar='\\')
    term = exact | word
    comparison_term = word + Literal(':') + term
    type_term = Word("type") + Literal(':') + Word(alphas)
    query_group = Group(Optional(type_term)) + Group(OneOrMore(Group(comparison_term)))
    return query_group


def tokenize(string):
    return get_grammar().parseString(string, parseAll=True).asList()