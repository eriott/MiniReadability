import unittest

from src.validators import UrlValidator


class UrlValidatorTest(unittest.TestCase):
    validator = UrlValidator()

    def test_is_valid_returns_True_on_valid_url(self):
        self.assertEqual(self.validator.is_valid('https://google.com'), True)

    def test_is_valid_returns_True_on_valid_url_with_slash_at_the_end_of_path(self):
        self.assertEqual(self.validator.is_valid('https://google.com/'), True)

    def test_is_valid_returns_True_on_url_with_path(self):
        self.assertEqual(self.validator.is_valid('https://google.com/some/path'), True)

    def test_is_valid_returns_True_on_url_with_parameters(self):
        self.assertEqual(self.validator.is_valid('https://google.com/some/path?any=parameter&other=one'), True)

    def test_is_valid_returns_False_on_random_string(self):
        self.assertEqual(self.validator.is_valid('any random string'), False)

    def test_is_valid_returns_False_on_url_without_scheme(self):
        self.assertEqual(self.validator.is_valid('google.com'), False)

    def test_is_valid_returns_False_on_number(self):
        self.assertEqual(self.validator.is_valid(123), False)


if __name__ == '__main__':
    unittest.main()
