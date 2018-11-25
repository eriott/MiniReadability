import unittest

from lxml import html

from src.HtmlToTextConverter import HtmlToTextConverter


class HtmlToTextConverterTest(unittest.TestCase):
    converter = HtmlToTextConverter()

    def test_convert_converts_html_with_given_rules(self):
        input = '<body><div><p>Text 1</p><p>Text 2</p><p>Text 3</p></div></body>'
        self.assertEqual(self.converter.convert(html.fromstring(input)), 'Text 1\n\nText 2\n\nText 3')

    def test_convert_converts_html_with_headers_with_given_rules(self):
        input = '' \
                '<body>' \
                    '<div>' \
                        '<h1>Header 1</h1>' \
                        '<h2>Header 2</h2>' \
                        '<h3>Header 3</h3>' \
                        '<h4>Header 4</h4>' \
                        '<h5>Header 5</h5>' \
                        '<h6>Header 6</h6>' \
                    '</div>' \
                '</body>'

        self.assertEqual(self.converter.convert(html.fromstring(input)),
                         'Header 1\n\nHeader 2\n\nHeader 3\n\nHeader 4\n\nHeader 5\n\nHeader 6')

    def test_convert_converts_html_with_links(self):
        input = '<body>' \
                    '<div>' \
                        '<a href=\'https://any.url\'>Link 1</a>' \
                        '<p>Text 1 <a href=\'https://other.url\'>Link 2</a></p>' \
                        '<p>Text 2</p>' \
                    '</div>' \
                '</body>'

        self.assertEqual(self.converter.convert(html.fromstring(input)), 'Link 1 [https://any.url]\n\nText 1 Link 2 [https://other.url]\n\nText 2')

    def test_convert_converts_does_not_add_href_when_link_has_no_href(self):
        input = '<body>' \
                    '<div>' \
                        '<a>Link 1</a>' \
                    '</div>' \
                '</body>'

        self.assertEqual(self.converter.convert(html.fromstring(input)), 'Link 1')