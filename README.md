plasticparser
=============

An Elastic Search Query Parser


```python
from plasticparser import plasticparser

query_string = 'type:candidates facets:[location] (name:"John Doe" starred:true) (python or java)'
global_filters = {
            'and': [{"client_id": 1},
                    {"user_id": 2}],
            'or': [],
            'not': [],
            'sort': [{"created_on": "desc"}]
        }
print plasticparser.get_query_dsl(query_string, global_filters)
```

```python
{
    'query': {
        'filtered': {
            'filter': {
                'bool': {
                    'must': [
                        {
                            'type': {'value': 'candidates' }
                        },
                        {
                            'term': {'client_id': 1}
                        },
                        {
                            'term': {'user_id': 2}
                        }
                    ],
                    'must_not': [],
                    'should': [
                        {
                            'term': {'assigned_to': ['/api/v1/users/5/']}
                        }
                    ]
                }
            },
            'query': {
                'query_string': {'query': u'(name:\\"John Doe\\" AND starred:true) AND (python OR java)'}
            }
        }
    },
    'facets': {
        'location': {
            'terms': {
                'field': 'location'
            }
        }
    },
    'sort': [
        {'created_on': 'desc'}
    ]
}
```
