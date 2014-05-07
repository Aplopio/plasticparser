# -*- coding: utf-8 -*-

from . import entities, tokenizer


def _construct_query(tokens):
    terms = entities.get_terms(tokens)
    return {
        "and": [term.get_query() for term in terms]
    }


def get_query_dsl(query_string):
    tokens = tokenizer.tokenize(query_string)
    return {
        "query": {
            "filtered": {
                "filter": _construct_query(tokens)
            }
        }
    }