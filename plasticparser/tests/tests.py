import unittest
from plasticparser.plasticparser import get_query_dsl


class PlasticParserTestCase(unittest.TestCase):
    def test_should_return_elastic_search_query_dsl_for_simple_search(self):
        query_string = 'title:hello AND description:world'
        elastic_query_dsl = get_query_dsl(query_string)
        expected_query_dsl = {
            "query": {
                "filtered": {
                    "filter": {
                        "and": [
                            {
                                "term": {"title": "hello"}
                            },
                            {
                                "term": {"description": "world"}
                            }
                        ]
                    }
                }
            }
        }
        self.assertEqual(elastic_query_dsl, expected_query_dsl)

if __name__ == '__main__':
    unittest.main()
