# -*- coding: utf-8 -*-

class Term(object):
    def __init__(self, token):
        self.token = token
        self.key = token[0]
        self.operator = token[1]
        self.value = token[2]

    def get_query(self):
        return {
            "term": {
                self.key: self.value
            }
        }


def get_terms(tokens):
    return [Term(token) for token in tokens if token]
