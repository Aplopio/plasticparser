# -*- coding: utf-8 -*-
from . import tokenizer


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
    global_filters = global_filters if global_filters else []

    expression = tokenizer.tokenize(query_string)

    # expression = Expression(query=expression.query,
    #                         type_filter=expression.type_filter,
    #                         filters=Filters(global_filters_dict=global_filters,
    #                                               type_filter=expression.type_filter))
    # return expression.get_query()
    pass

def get_document_types(query_string):
    """
    returns all the document types in a given query string
     param: query_string : an expression of the form
     type: person title:foo AND description:bar
     where type corresponds to an elastic search document type
    """
    # expression = tokenizer.tokenize(query_string)[0]
    # return [expression.type_filter.value]
    pass
