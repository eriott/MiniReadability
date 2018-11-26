import re
from urllib.parse import urlparse

from lxml import html

import config
from src import utils


class HtmlToTextConverter:
    text_tags_pattern = re.compile('^h[1-6]|a|p|ul|li$')

    def _format(self, elem):
        elem.text = re.sub('[\r\n\t]+', '', elem.text) if bool(elem.text) else ''
        elem.tail = re.sub('[\r\n\t]+', '', elem.tail) if bool(elem.tail) else ''
        content = elem.text_content()
        for subnode in elem.getchildren():
            subnode.drop_tree()

        format = utils.match_keys(elem.tag, config.format_rules)

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

            if utils.match_items(elem.tag, config.not_format_tags):
                continue

            if isinstance(elem, html.HtmlElement):
                self._search_text(elem)

            if utils.match_items(elem.tag, config.text_tags):
                self._format(elem)

        output = node.text_content()
        return output

    def convert(self, html):
        output = self._search_text(html)
        wrapped = utils.wrap(output, config.max_line_width)
        return re.sub('\n\n+', '\n\n', wrapped).strip()


class UrlToFilepathConverter:
    replace_symbols = '[\:*?"<>|+]+'

    def convert(self, url):
        file_type = '.txt'

        parsed_url = urlparse(url)
        host = re.sub(self.replace_symbols, '_', parsed_url.netloc)
        path = re.sub(self.replace_symbols, '_', parsed_url.path)

        components = list(filter(None, path.split('/')))
        if components:
            last_component = components[-1]
            other_components = components[:-1]
            index_of_dot = last_component.rfind('.')
            if index_of_dot > -1:
                last_component = last_component[:index_of_dot] + file_type
            else:
                last_component = last_component + file_type
            return host + (('/' + '/'.join(other_components)) if other_components else '') + '/' + last_component
        else:
            return host + file_type
