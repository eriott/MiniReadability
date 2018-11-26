import unittest

from src.parser import MiniReadabilityParser


class MiniReadabilityParserTest(unittest.TestCase):
    parser = MiniReadabilityParser()
    #
    # def test_parse_parses_html(self):
    #     input = '<body><div><p>Text</p></div></body>'
    #     self.assertEqual(self.parser.parse(input), 'Text')
    #
    # def test_parse_parses_html2(self):
    #     input = '<body><div><p>Text 1</p><p>Text 2</p><p>Text 3</p></div></body>'
    #     self.assertEqual(self.parser.parse(input), 'Text 1\n\nText 2\n\nText 3')

    # def test_parse_parses_html3(self):
    #     input = '<body><div><h1>Header 1</h1><p>Text 1</p><p>Text 2</p><p>Text 3</p></div></body>'
    #     self.assertEqual(self.parser.parse(input), 'Header 1\n\nText 1\n\nText 2\n\nText 3')

    def test_parse_parses_html3(self):
        input = '<body><div><h1>Header 1</h1><p>Text 1</p><div><p>Text 2</p><p>Text 3</p></div></div></body>'
        self.assertEqual(self.parser.parse(input), 'Header 1\n\nText 1\n\nText 2\n\nText 3')

    # def test_parse_parses_all_header_types(self):
    #     input = '<body><div><h1>Header 1</h1><h2>Header 2</h2><h3>Header 3</h3><h4>Header 4</h4><h5>Header 5</h5><h6>Header 6</h6></div></body>'
    #     self.assertEqual(self.parser.parse(input), 'Header 1\n\nHeader 2\n\nHeader 3\n\nHeader 4\n\nHeader 5\n\nHeader 6')
