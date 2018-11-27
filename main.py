import sys

import requests

from src.converters import UrlToFilepathConverter
from src.io import TextFileWriter
from src.parser import MiniReadabilityParser
from src.validators import UrlValidator

if len(sys.argv) == 2:
    url = sys.argv[1]
else:
    print('Wrong number of parameters.')
    print('Usage: python main.py https://habr.com/company/mailru/blog/429186')
    exit(1)

try:
    if not (UrlValidator().is_valid(url)):
        print('Skip invalid URL', url)
        exit(1)

    print('Process URL', url)
    page = requests.get(url)
    page.raise_for_status()
    encoding = page.encoding if page.encoding else 'utf-8'

    if not page.content:
        raise Exception('No content received from URL')

    output = MiniReadabilityParser().parse(page.content.decode(page.encoding), url)

    file_path = UrlToFilepathConverter().convert(url)
    TextFileWriter().write(file_path, output)
    exit(0)
except UnicodeDecodeError as e:
    print('Can not decode page content with encoding', encoding)
except requests.exceptions.RequestException as e:
    print('Can not get page.', e)
except Exception as e:
    print('Error has occurred:', e)
finally:
    exit(1)
