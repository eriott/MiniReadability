import unittest
from lxml import html

from src.parser import RelativeLinksProcessor


class RelativeLinksProcessorTest(unittest.TestCase):
    base_url = 'https://google.com'
    processor = RelativeLinksProcessor()

    def test_process_does_nothing_when_link_has_scheme_and_host(self):
        input = html.fromstring('<div><a href=\'https://google.com\'>Click me</a></div>')

        self.processor.process(input, self.base_url)

        link = input.getchildren()[0]
        self.assertEqual(link.tag, 'a')
        self.assertEqual(link.attrib['href'], 'https://google.com')

    def test_process_extend_relative_url_to_absolute(self):
        input = html.fromstring('<div><a href=\'/local/path\'>Click me</a></div>')

        self.processor.process(input, self.base_url)

        link = input.getchildren()[0]
        self.assertEqual(link.tag, 'a')
        self.assertEqual(link.attrib['href'], 'https://google.com/local/path')

    def test_process_extend_relative_url_to_absolute_with_hash_in_path(self):
        input = html.fromstring('<div><a href=\'#anchor\'>Click me</a></div>')

        self.processor.process(input, self.base_url)

        link = input.getchildren()[0]
        self.assertEqual(link.tag, 'a')
        self.assertEqual(link.attrib['href'], 'https://google.com/#anchor')

