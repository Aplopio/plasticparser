# -*- coding: utf-8 -*-

from . import entities, tokenizer


def _construct_query(tokens):
    filters = entities.Filters(tokens)
    query_dsl = {}
    if filters.has_type_filter():
        query_dsl['and'] = [filters.get_type_filter().get_query()]
    query_dsl['or'] = [_filter.get_query() for _filter in filters.get_term_filters()]
    return query_dsl


def get_query_dsl(query_string):
    tokens = tokenizer.tokenize(query_string)
    return {
        "query": {
            "filtered": {
                "filter": _construct_query(tokens)
            }
        }
    }

def get_document_types(query_string):
    tokens = tokenizer.tokenize(query_string)
    filters = entities.Filters(tokens)
    return [filters.get_type_filter().value] if filters.has_type_filter() else []
