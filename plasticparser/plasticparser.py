# -*- coding: utf-8 -*-
from . import tokenizer

def get_query_dsl(query_string, global_filters=None, facets_query_size=20):
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
    global FACETS_QUERY_SIZE
    FACETS_QUERY_SIZE = facets_query_size

    global_filters = global_filters if global_filters else {}
    expression = tokenizer.tokenize(query_string)
    bool_lists = expression['query']['filtered']['filter']['bool']
    [bool_lists['should'].append({"term": orele}) for orele in global_filters.get('or', [])]
    [bool_lists['must'].append({"term": andele}) for andele in global_filters.get('and', [])]
    [bool_lists['must_not'].append({"term": notele}) for notele in global_filters.get('not', [])]
    expression['sort'] = global_filters.get('sort', [])
    return expression

def get_document_types(query_string):
    """
    returns all the document types in a given query string
     param: query_string : an expression of the form
     type: person title:foo AND description:bar
     where type corresponds to an elastic search document type
    """
    expression = tokenizer.tokenize(query_string)
    must_filters = expression['query']['filtered']['filter']['bool']['must']
    return [filter['type']['value'] for filter in must_filters if filter.keys()[0]=='type']
