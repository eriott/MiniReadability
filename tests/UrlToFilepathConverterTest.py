import unittest

from src.converters import UrlToFilepathConverter


class UrlToFilepathConverterTest(unittest.TestCase):
    parser = UrlToFilepathConverter()

    def test_convert_returns_filename_when_only_scheme_and_domain_in_url(self):
        self.assertEqual(self.parser.convert('https://google.com'), 'google.com.txt')

    def test_convert_returns_directory_when_url_has_path(self):
        self.assertEqual(self.parser.convert('https://google.com/some/long/very/long/path'), 'google.com/some/long/very/long/path.txt')

    def test_convert_returns_directory_and_replaces_filetype_in_url_with_txt(self):
        self.assertEqual(self.parser.convert('https://google.com/some/path.with.dots.html'), 'google.com/some/path.with.dots.txt')

    def test_convert_returns_directory_and_removes_slash_at_the_end_of_path(self):
        self.assertEqual(self.parser.convert('https://google.com/some/long/very/long/path/'), 'google.com/some/long/very/long/path.txt')

    def test_replaces_not_allowed_symbols_with_underscore(self):
        self.assertEqual(self.parser.convert('https://google.com/so+me/l<o>ng/very/lo:ng/p*ath'), 'google.com/so_me/l_o_ng/very/lo_ng/p_ath.txt')

    def test_replaces_not_allowed_symbols_with_underscore1(self):
        self.assertEqual(self.parser.convert('https://google.com/'), 'google.com.txt')

    def test_convert_converts_domain_with_one_path_component_properly(self):
        self.assertEqual(self.parser.convert('https://google.com/index.html'), 'google.com/index.txt')
