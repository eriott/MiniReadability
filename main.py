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

    print('Process URL', url)

    page = requests.get(url)
    # testPage = '<body><div><h2>Header</h2><p>Hello <span>world</span> <a href=\'google.com\'>Click here</a></p></div></body>'
    output = MiniReadabilityParser().parse(page.content.decode(page.encoding))

    output_filename = UrlFilepathParser().parse(url)
    TextFileWriter().write(output_filename, output)
    print('File saved to', output_filename)
    print()
