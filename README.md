plasticparser
=============

An Elastic Search Query Parser

```
from plasticparser import plasticparser

query_string = 'type:help and title:hello description:"world"'
global_filters = {
            'and': [{"client_id": 1},
                    {"user_id": 2}],
            'or': [],
            'not': []
        }
print plasticparser.get_query_dsl(query_string, global_filters)

{
    "query": {
        "filtered": {
            "query": {
                "query_string": {
                    "query": 'title:hello description:\\"world\\"'
                }
            },
            "filter": {
                "bool": {
                    "must": [
                        {
                            "term": {"client_id": 1}
                        },
                        {
                            "term": {"user_id": 2}
                        },
                        {
                            "type": {"value": "help"}
                        },
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
    }
}

```
