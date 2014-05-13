# -*- coding: utf-8 -*-

from . import entities, tokenizer
from .entities import Expression, Query, Filters


def _map_global_filters_to_token_list(global_filters):
    return [[glob_filter.keys()[0], ':', glob_filter[glob_filter.keys()[0]]]
            for glob_filter in global_filters] if global_filters else []


def _get_filter_tokens(type_filter_tokens, global_filters=None):
    global_filters = global_filters if global_filters else []
    type_filter_tokens = [type_filter_tokens] if type_filter_tokens else []
    global_filter_tokens = _map_global_filters_to_token_list(global_filters)
    return global_filter_tokens + type_filter_tokens


def get_query_dsl(query_string, global_filters=None):
    """
    returns an elasticsearch query dsl for a query string
    param: query_string : an expression of the form
     type: person title:foo AND description:bar
     where type corresponds to an elastic search document type
     which gets added as a filter

    param: global_filters : a dictionary of the form
     {user_id: 1234}. This gets added as a filter to the query
     so that the query can be narrowed down to fewer documents.
     It is translated into an elastic search term filter.
    """
    tokens = tokenizer.tokenize(query_string)
    query_tokens = tokens[1][0]
    filter_tokens = _get_filter_tokens(tokens[0], global_filters)
    expression = Expression(query=(Query(query_tokens)),
                            filters=(Filters(filter_tokens)))
    return expression.get_query()


def get_document_types(query_string):
    """
    returns all the document types in a given query string
     param: query_string : an expression of the form
     type: person title:foo AND description:bar
     where type corresponds to an elastic search document type
    """
    tokens = tokenizer.tokenize(query_string)
    filters = entities.Filters(_get_filter_tokens(tokens[0]))
    return [filters.get_type_filters()[0].value] if filters.has_type_filters() else []
