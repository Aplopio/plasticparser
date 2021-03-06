plasticparser
=============

[![Circle CI](https://circleci.com/gh/Aplopio/plasticparser/tree/master.svg?style=svg)](https://circleci.com/gh/Aplopio/plasticparser/tree/master)

An Elastic Search Query Parser

### Installation

```
$ pip install plasticparser
```

### Usage


```python
from plasticparser import plasticparser

query_string = 'type:candidates (name:"John Doe" starred:true) (python or java) facets:[location]'
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
                    'must_not': []
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
