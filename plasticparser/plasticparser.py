import tokenizer


def get_query_dsl(query_string):
    tokens = tokenizer.tokenize(query_string)
