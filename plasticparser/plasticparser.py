# -*- coding: utf-8 -*-

from . import entities, tokenizer


def _construct_query(filters):
    return [_filter.get_query() for _filter in filters.get_term_filters()]


def _construct_filtered_query(filters):
    query_dsl = {}
    if filters.has_type_filter():
        query_dsl['and'] = [filters.get_type_filter().get_query()]
    return query_dsl


def get_query_dsl(query_string):
    tokens = tokenizer.tokenize(query_string)
    filters = entities.Filters(tokens)
    return {
        "query": {
            "filtered": {
                "query": _construct_query(filters),
                "filter": _construct_filtered_query(filters)
            }
        }
    }


def get_document_types(query_string):
    tokens = tokenizer.tokenize(query_string)
    filters = entities.Filters(tokens)
    return [filters.get_type_filter().value] if filters.has_type_filter() else []
