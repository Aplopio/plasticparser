# -*- coding: utf-8 -*-

from . import entities, tokenizer


def get_query_dsl(query_string):
    tokens = tokenizer.tokenize(query_string)
    query = entities.Query(tokens[1])
    filter_tokens = [tokens[0]] if tokens[0] else []
    filters = entities.Filters(filter_tokens)
    return {
        "query": {
            "filtered": {
                "query":  query.get_query(),
                "filter": filters.get_query()
            }
        }
    }


def get_document_types(query_string):
    tokens = tokenizer.tokenize(query_string)
    filters = entities.Filters([tokens[0]])
    return [filters.get_type_filters()[0].value] if filters.has_type_filter() else []
