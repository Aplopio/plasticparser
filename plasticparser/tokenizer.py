# -*- coding: utf-8 -*-

from pyparsing import Word, Literal, alphas, Group, Optional


def get_grammar():
    unicode_printables = u''.join(unichr(c) for c in xrange(65536))
    type_term = Literal("type") + ':' + Word(alphas)
    query_group = Group(Optional(type_term)) + Group(Word(unicode_printables))
    return query_group


def tokenize(string):
    return get_grammar().parseString(string.replace('\n', '').strip(), parseAll=True).asList()