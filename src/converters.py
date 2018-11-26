import re
import textwrap
from urllib.parse import urlparse

from lxml import html

import config
from src import utils


class HtmlToTextConverter:
    text_tags_pattern = re.compile('^h[1-6]|a|p|ul|li$')

    def _format(self, elem):
        elem.text = re.sub('[ \r\n\t]+', ' ', elem.text) if bool(elem.text) else ''
        elem.tail = re.sub('[ \r\n\t]+', ' ', elem.tail) if bool(elem.tail) else ''
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

            if isinstance(elem, html.HtmlElement):
                self._search_text(elem)

            if utils.match_items(elem.tag, config.text_tags):
                self._format(elem)

        output = node.text_content()
        return output

    def convert(self, html):
        output = self._search_text(html)
        wrapped = '\n'.join(['\n'.join(textwrap.wrap(x, width=config.max_line_width)) for x in output.split('\n')])

        return re.sub('\n\n+', '\n\n', wrapped).strip()


class UrlToFilepathConverter:
    def convert(self, url):
        file_type = '.txt'
        parsed_url = urlparse(url)

        if bool(parsed_url.path):
            components = list(filter(None, parsed_url.path.split('/')))
            last_component = components[-1]
            components = components[:-1]
            index_of_dot = last_component.rfind('.')
            if index_of_dot > -1:
                last_component = last_component[:index_of_dot] + file_type
            else:
                last_component = last_component + file_type
            return parsed_url.netloc + '/' + '/'.join(components) + '/' + last_component
        else:
            return parsed_url.netloc + file_type