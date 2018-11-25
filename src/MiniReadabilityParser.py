import re
import textwrap

from lxml import html

from src.TextFileWriter import TextFileWriter


class Element:
    sentences_count = None
    sentences_avg_length = None
    repeated_tags_count = None
    non_text_tags_count = None

    def __init__(self, elem):
        self.element = elem
        text = re.sub('[ \n\t]+', ' ', elem.text_content())

        self.sentences = [x.strip() for x in list(filter(None, text.split('.')))]
        self.sentences_count = len(self.sentences)
        self.sentences_avg_length = sum(map(lambda x: len(x), self.sentences)) / len(self.sentences) if len(self.sentences) > 0 else 0
        self.cost = self.sentences_count * 10 + self.sentences_avg_length * 0.05


class MiniReadabilityParser:
    def search_p(self, tree):
        for i in range(len(tree)):
            ps = tree[i].xpath('.//p')
            for j in range(len(ps)):
                print(ps[j].text_content())  # все p теги

    # def _search_text(self, node):
    #     output = ''
    #     headers_pattern = "^h[1-6]$"
    #     headers = re.compile(headers_pattern)
    #     # for elem in nodes:
    #     for elem in node.getchildren():
    #         if not (isinstance(elem.tag, str)):
    #             continue
    #
    #         if headers.match(elem.tag):
    #             output += '\n'.join(textwrap.wrap(elem.text_content(), width=80))
    #             output += '\n\n'
    #         elif elem.tag == 'p':
    #             paragraph = elem.text_content()
    #             for p_child in elem.getchildren():
    #                 if p_child.tag == 'a':
    #                     paragraph += '[' + p_child.get('href') + ']'
    #
    #             output += '\n'.join(textwrap.wrap(paragraph, width=80)) + '\n\n'
    #             print(type(elem))
    #         elif isinstance(elem, html.HtmlElement):
    #             output += self._search_text(elem)
    #     return output

    def _format(self, elem):
        content = re.sub('[ \n\t]+', ' ', elem.text_content().strip())
        for subnode in elem.getchildren():
            subnode.drop_tree()
        elem.text = content + '\n\n'

    def _search_text(self, node):
        headers_pattern = "^h[1-6]$"
        headers = re.compile(headers_pattern)
        # for elem in nodes:
        for elem in node.getchildren():
            if not (isinstance(elem.tag, str)):
                continue

            if isinstance(elem, html.HtmlElement):
                self._search_text(elem)

            if headers.match(elem.tag):
                self._format(elem)
            elif elem.tag == 'p':
                self._format(elem)
            elif elem.tag == 'a':
                link = ' [' + str(elem.get('href')) +  ']' if bool(elem.get('href')) else ''
                content = elem.text_content().strip()
                for subnode in elem.getchildren():
                    subnode.drop_tree()
                elem.text = content + link

        print(node.tag, ':', node.text)
        node.text = re.sub('[ \n\t]+', ' ', node.text.strip()) if bool(node.text) else ''
        output = node.text_content().strip()
        return '\n'.join(['\n'.join(textwrap.wrap(x, width=80)) for x in output.split('\n')])

    elements = []

    def register_divs(self, elem):
        children = elem.getchildren()
        for el in children:
            if el.tag == 'script' or el.tag == 'style':
                el.drop_tree()
                continue

            self.register_divs(el)
            if el.tag == 'div':
                el.drop_tree()
                self.elements.append(Element(el))

    def parse(self, content):
        tree = html.fromstring(content)

        body_node = tree.body

        self.register_divs(body_node)
        temp = ''
        print('Elements', len(self.elements))
        for e in self.elements:
            temp += '---\n\n'
            temp += 'Sentences ' + str(e.sentences) + '\n\n'
            temp += 'Sentences count ' + str(e.sentences_count) + '\n\n'
            temp += 'Sentences avg length ' + str(e.sentences_avg_length) + '\n\n'
            temp += 'Score ' + str(e.cost) + '\n\n'
            temp += e.element.text_content() + '\n\n'
            temp += '---\n\n'
            temp += '---\n\n'

        TextFileWriter().write('res.txt', temp)

        sorted_elements = list(sorted(self.elements, key=lambda x: x.cost, reverse=True))

        content = sorted_elements[0].element

        # TextFileWriter().write('res1.txt', content.text + content.tail)


        output = self._search_text(content)


        # articles = body_node.xpath('//article/h1 | //article/div/p | //article/p')
        #
        # print('Found <article>:', len(articles) > 0)
        # if len(articles) > 0:
        #     output = self._search_text(articles)
        # else:
        #     # divs_with_ps = body_node.xpath('//div')
        #     output = self._search_text(body_node)

        return output.strip()
