# -*- coding: utf-8 -*-

from pyparsing import Word, QuotedString, oneOf, CaselessLiteral, White, Literal, OneOrMore, Optional

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
    if len(tokens) == 2 and tokens[0].isspace():
        tokens[0] = 'and'
    return u' '.join(tokens)

def _parse_one_or_more_logical_expressions(tokens):
    return u' '.join(tokens)


def _construct_grammar():
    unicode_printables = u''.join(unichr(c) for c in xrange(65536)
                                  if not unichr(c).isspace())
    word = Word(unicode_printables)
    quoted_word = QuotedString('"', unquoteResults=True, escChar='\\')
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
        _parse_paren_base_logical_expression) | base_logical_expression.setParseAction(_parse_base_logical_expression)

    expression = OneOrMore(Optional(logical_operator)+logical_expression).setParseAction(_parse_one_or_more_logical_expressions)

    '''
    expression = ('(' + (logical_expression + logical_operator + logical_expression) + ')').setParseAction(_parse_paren_logincal_expression) | (
        logical_expression + logical_operator + logical_expression)
    '''
    return expression


grammar = _construct_grammar()


def tokenize(query_string):
    return grammar.parseString(query_string.replace('\n', '').strip(),
                               parseAll=True).asList()[0]
