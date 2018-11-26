import re

import config
from src import utils


class WeightElement:
    def __init__(self, elem):
        punctuation_pattern = '[,:‐–—;«»"\'()]'
        sentence_pattern = '\s*[^.!?]+[.!?]'

        chars_per_punctuation_avg_count = 40 # посчитано по нескольким статьям

        self.element = elem
        self.text = re.sub('[ \r\n\t]+', ' ', elem.text_content())
        self.sentences = [x.strip() for x in list(filter(None, re.findall(sentence_pattern, self.text)))]
        self.sentences_count = len(self.sentences)
        self.sentences_avg_length = sum(map(lambda x: len(x), self.sentences)) / self.sentences_count if self.sentences_count > 0 else 0 # средняя длина предложения в символах
        self.punctuation_count = len(re.findall(punctuation_pattern, self.text)) # количество знаков препинания во всем тексте
        self.chars_per_punctuation = len(self.text) / (self.punctuation_count + 1) # через каждые сколько символов встречается знак пунктуации

        self.chars_per_punctuation_avg_ratio = 0 # соотношения данного среднего с "идеальным"
        if chars_per_punctuation_avg_count > self.chars_per_punctuation:
            self.chars_per_punctuation_avg_ratio = chars_per_punctuation_avg_count / self.chars_per_punctuation if self.chars_per_punctuation else 1
        else:
            self.chars_per_punctuation_avg_ratio = self.chars_per_punctuation / chars_per_punctuation_avg_count

        self.cost = self.sentences_count * 10 + self.sentences_avg_length * 0.05 - (self.chars_per_punctuation_avg_ratio - 1) * 10


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
        self.register_containers(html.body)

        content = None
        if self.elements:
            content = max(self.elements, key=lambda x: x.cost)

        return content.element
