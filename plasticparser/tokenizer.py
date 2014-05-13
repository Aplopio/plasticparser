# -*- coding: utf-8 -*-

from pyparsing import Word, Literal, alphas, Group, Optional, quotedString

from . import entities


def get_grammar():
    unicode_printables = u''.join(unichr(c) for c in xrange(65536))
    word = Word(unicode_printables)
    type_term = Literal("type") + ':' + Word(alphas)
    exact = quotedString.setParseAction(entities._sanitize_term_value)
    query_group = Group(Optional(type_term)) + Group(exact | word)
    return query_group


def tokenize(string):
    return get_grammar().parseString(string.replace('\n', '').strip(), parseAll=True).asList()