# -*- coding: utf-8 -*-

from pyparsing import Word, Literal, alphas, QuotedString, Group, ZeroOrMore


def get_grammar():
    word = Word(alphas)
    exact = QuotedString('"', unquoteResults=True, escChar='\\')
    term = exact | word
    comparison_term = word + Literal(':') + term
    grammar = Group(comparison_term) + Group(ZeroOrMore(comparison_term))
    return grammar


def tokenize(string):
    return get_grammar().parseString(string, parseAll=True).asList()