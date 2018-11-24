import unittest

from src.UrlFilepathParser import UrlFilepathParser


class UrlFilepathParserTest(unittest.TestCase):
    parser = UrlFilepathParser()

    def test_parse_returns_filename_when_only_scheme_and_domain_in_url(self):
        self.assertEqual(self.parser.parse('https://google.com'), 'google.com.txt')

    def test_parse_returns_directory_when_url_has_path(self):
        self.assertEqual(self.parser.parse('https://google.com/some/long/very/long/path'), 'google.com/some/long/very/long/path.txt')

    def test_parse_returns_directory_and_replaces_filetype_in_url_with_txt(self):
        self.assertEqual(self.parser.parse('https://google.com/some/path.with.dots.html'),'google.com/some/path.with.dots.txt')

    def test_parse_returns_directory_and_removes_slash_at_the_end_of_path(self):
        self.assertEqual(self.parser.parse('https://google.com/some/long/very/long/path/'), 'google.com/some/long/very/long/path.txt')

if __name__ == '__main__':
    unittest.main()
