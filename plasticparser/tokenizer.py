from pyparsing import Word, Literal, alphas


def get_grammar():
    grammar = Word(alphas) + Literal(':') + Word(alphas)
    return grammar


def tokenize(string):
    return get_grammar().parseString(string)