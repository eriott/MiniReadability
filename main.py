import sys

import requests

from src.MiniReadabilityParser import MiniReadabilityParser
from src.TextFileWriter import TextFileWriter
from src.UrlFilepathParser import UrlFilepathParser
from src.UrlValidator import UrlValidator

if sys.argv[1] == '-f':
    filename = sys.argv[2]
    with open(filename) as f:
        urls = [x.strip() for x in f.readlines()]
else:
    urls = [sys.argv[1]]

for url in urls:
    if not (UrlValidator().is_valid(url)):
        print('Skip invalid URL', url)
        continue

    try:
        print('Process URL', url)
        page = requests.get(url)
        encoding = page.encoding if page.encoding else 'utf-8'

        if not page.content:
            raise Exception('No content received from URL')

        output = MiniReadabilityParser().parse(page.content.decode(page.encoding), url)

        file_path = UrlFilepathParser().parse(url)
        TextFileWriter().write(file_path, output)
        print()
    except UnicodeDecodeError as e:
        print('Can not decode page content with encoding', encoding)
    except requests.exceptions.RequestException as e:
        print('Can not get page.')
    except Exception as e:
        print('Error has occurred:', e)