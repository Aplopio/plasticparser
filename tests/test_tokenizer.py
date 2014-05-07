import unittest
from plasticparser import tokenizer


class TokeinzerTestCase(unittest.TestCase):
    def test_should_tokenize_simple_string(self):
        tokens = tokenizer.tokenize('title:abc')
        self.assertEqual(tokens.asList(), ['title', ':', 'abc'])


if __name__ == '__main__':
    unittest.main()
