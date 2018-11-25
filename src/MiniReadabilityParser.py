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
        text = re.sub('[ \r\n\t]+', ' ', elem.text_content())

        self.sentences = [x.strip() for x in list(filter(None, text.split('.')))]
        self.sentences_count = len(self.sentences)
        self.sentences_avg_length = sum(map(lambda x: len(x), self.sentences)) / len(self.sentences) if len(
            self.sentences) > 0 else 0
        self.cost = self.sentences_count * 10 + self.sentences_avg_length * 0.05


class MiniReadabilityParser:
    text_tags_pattern = re.compile('^h[1-6]|a|p|ul|li$')
    format_rules = {
        'p': '{val}\n\n',
        'h[1-6]': '{val}\n\n',
        'a': lambda params: '{val} [{href}]' if 'href' in params else '{val}',
        'li': ' - {val}\n',
        'ul': '\n{val}\n'
    }

    def _format(self, elem):
        print('Format tag', elem.tag, ', text:', elem.text, ', text_content:', elem.text_content())
        elem.text = re.sub('[ \r\n\t]+', ' ', elem.text) if bool(elem.text) else ''
        elem.tail = re.sub('[ \r\n\t]+', ' ', elem.tail) if bool(elem.tail) else ''
        content = elem.text_content()
        for subnode in elem.getchildren():
            subnode.drop_tree()

        formats = [(key, value) for key, value in self.format_rules.items() if re.compile(key).match(elem.tag)]
        format = None
        if len(formats) > 0:
            format = formats[0]
        if format:
            attrs = {}
            for att in elem.attrib:
                attrs[att] = elem.attrib[att]
            if callable(format[1]):
                params = {'val': content, **attrs}
                elem.text = format[1](params).format(**params)
            else:
                elem.text = format[1].format(**{'val': content, **attrs})
        else:
            elem.text = content

    def _search_text(self, node):
        for elem in node.getchildren():
            if not (isinstance(elem.tag, str)):
                continue

            if isinstance(elem, html.HtmlElement):
                self._search_text(elem)

            if self.text_tags_pattern.match(elem.tag):
                self._format(elem)

        print(node.tag, ':', node.text)
        # node.text = re.sub('[ \n\t]+', ' ', node.text.strip()) if bool(node.text) else ''
        output = node.text_content()
        return output

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

        text = self._search_text(content)
        output = re.sub('\r\n', '\n', text)
        wrapped = '\n'.join(['\n'.join(textwrap.wrap(x, width=80)) for x in output.split('\n')])
        wrapped = re.sub('\n\n+', '\n\n', wrapped)

        return wrapped.strip()
