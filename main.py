import sys
import requests
import re
import textwrap
from lxml import html
from urllib.parse import urlparse


def search_p(tree):
    for i in range(len(tree)):
        ps = tree[i].xpath('.//p')
        for j in range(len(ps)):
            print(ps[j].text_content())  # все p теги


def search_text(nodes):
    output = ''
    headers_pattern = "^h[1-6]$"
    headers = re.compile(headers_pattern)
    # '\n'.join(textwrap.wrap(output, width=80))
    for node in nodes:
        for elem in node.getchildren():
            if not(isinstance(elem.tag, str)):
                continue

            if headers.match(elem.tag):
                output += '\n'.join(textwrap.wrap(elem.text_content(), width=80))
                output += '\n\n'
            elif elem.tag == 'p':
                paragraph = elem.text_content()
                for p_child in elem.getchildren():
                    if p_child.tag == 'a':
                        paragraph += '[' + p_child.get('href') + ']'

                output += '\n'.join(textwrap.wrap(paragraph, width=80)) + '\n\n'
    return output

    # for i in range(len(tree)):
    #     ps = tree[i].xpath('.//p')
    #     for j in range(len(ps)):
    #         print(ps[j].text_content())  # все p теги


if sys.argv[1] == '-f':
    filename = sys.argv[2]
    with open(filename) as f:
        urls = [x.strip() for x in f.readlines()]
else:
    urls = [sys.argv[1]]

for url in urls:
    print('Process URL', url)
    print()
    page = requests.get(url)
    encode = page.encoding

    # testPage = '<body><div><h2>Header</h2><p>Hello <span>world</span> <a href=\'google.com\'>Click here</a></p></div></body>'

    # tree = html.fromstring(testPage)
    tree = html.fromstring(page.content.decode(encode))

    bodyNode = tree.xpath('//body')[0]

    # Try to find <article> first of all

    articles = bodyNode.xpath('//article')
    output = ''

    print('Found <article>:', len(articles) > 0)
    if len(articles) > 0:
        output = search_text(articles)
    else:
        divsWithPs = bodyNode.xpath('//div[p]')
        output = search_text(divsWithPs)

    print()

    output_filename = urlparse(url).path.replace("/",u'\u2215')
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write(output)
