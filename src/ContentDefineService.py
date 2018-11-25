import re

import config
from src import utils
from src.TextFileWriter import TextFileWriter


class WeightElement:
    sentences_count = None
    sentences_avg_length = None
    repeated_tags_count = None
    non_text_tags_count = None
    punctuation_count = None

    def __init__(self, elem):
        self.element = elem
        text = re.sub('[ \r\n\t]+', ' ', elem.text_content())

        self.sentences = [x.strip() for x in list(filter(None, text.split('.')))]
        self.sentences_count = len(self.sentences)
        self.sentences_avg_length = sum(map(lambda x: len(x), self.sentences)) / len(self.sentences) if len(self.sentences) > 0 else 0
        self.punctuation_count = len(re.findall(',:‐–—;', text))
        self.cost = self.sentences_count * 10 + self.sentences_avg_length * 0.05 + self.punctuation_count * 5


class ContentDefineService:
    elements = []

    def register_containers(self, elem):
        children = elem.getchildren()
        for el in children:
            if not(isinstance(el.tag, str)):
                el.drop_tree()
                continue

            if utils.match_items(el.tag, config.ignore_tags):
                el.drop_tree()
                continue

            self.register_containers(el)
            if utils.match_items(el.tag, config.container_tags):
                el.drop_tree()
                self.elements.append(WeightElement(el))

    def get_content(self, html):
        body_node = html.body

        self.register_containers(body_node)
        temp = ''
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

        return content
