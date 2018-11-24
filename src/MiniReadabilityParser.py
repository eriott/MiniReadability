import re
import textwrap

from lxml import html


class MiniReadabilityParser:
    def search_p(self, tree):
        for i in range(len(tree)):
            ps = tree[i].xpath('.//p')
            for j in range(len(ps)):
                print(ps[j].text_content())  # все p теги

    def _search_text(self, node):
        output = ''
        headers_pattern = "^h[1-6]$"
        headers = re.compile(headers_pattern)
        # for elem in nodes:
        for elem in node.getchildren():
            if not (isinstance(elem.tag, str)):
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
                print(type(elem))
            elif isinstance(elem, html.HtmlElement):
                output += self._search_text(elem)
        return output

    def parse(self, content):
        tree = html.fromstring(content)

        body_node = tree.xpath('//body')[0]

        articles = body_node.xpath('//article/h1 | //article/div/p | //article/p')

        print('Found <article>:', len(articles) > 0)
        if len(articles) > 0:
            output = self._search_text(articles)
        else:
            # divs_with_ps = body_node.xpath('//div')
            output = self._search_text(body_node)

        return output.strip()
