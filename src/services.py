import re

import config
from src import utils
from src.io import TextFileWriter


class WeightElement:
    def __init__(self, elem):
        punctuation_pattern = '[,:‐–—;«»"\'()]'
        sentence_pattern = '\s*[^.!?]+[.!?]'

        word_avg_length = 6.5
        sentence_avg_length = 30
        chars_per_punctuation_avg_count = 40

        self.element = elem
        self.text = re.sub('[ \r\n\t]+', ' ', elem.text_content())
        self.sentences = [x.strip() for x in list(filter(None, re.findall(sentence_pattern, self.text)))]
        self.sentences_count = len(self.sentences)
        self.sentences_avg_length = sum(map(lambda x: len(x), self.sentences)) / len(self.sentences) if len(self.sentences) > 0 else 0
        self.punctuation_count = len(re.findall(punctuation_pattern, self.text))
        self.chars_per_punctuation = len(self.text) / (self.punctuation_count + 1)

        self.param = 0
        if chars_per_punctuation_avg_count > self.chars_per_punctuation:
            self.param = chars_per_punctuation_avg_count / self.chars_per_punctuation if self.chars_per_punctuation else 1
        else:
            self.param = self.chars_per_punctuation / chars_per_punctuation_avg_count

        self.cost = self.sentences_count * 10 + self.sentences_avg_length * 0.05 - (self.param - 1) * 100


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
            temp += 'Punctuation count ' + str(e.punctuation_count) + '\n\n'
            temp += 'Text length ' + str(len(e.text)) + '\n\n'
            temp += 'Chars Per Punctuation' + str(e.chars_per_punctuation) + '\n\n'
            temp += 'Param' + str(e.param) + '\n\n'
            temp += 'Score ' + str(e.cost) + '\n\n'
            temp += e.element.text_content() + '\n\n'
            temp += '---\n\n'
            temp += '---\n\n'

        TextFileWriter().write('res.txt', temp)

        sorted_elements = list(sorted(self.elements, key=lambda x: x.cost, reverse=True))

        content = sorted_elements[0].element

        return content
