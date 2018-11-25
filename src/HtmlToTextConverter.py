import re
import textwrap

from lxml import html


class HtmlToTextConverter:
    text_tags_pattern = re.compile('^h[1-6]|a|p|ul|li$')
    format_rules = {
        'p': '{val}\n\n',
        'h[1-6]': '{val}\n\n',
        'a': lambda params: '{val} [{href}]' if 'href' in params else '{val}',
        'li': ' - {val}\n',
        'ul': '\n{val}\n'
    }

    def _format(self, elem):
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

        output = node.text_content()
        return output

    def convert(self, html):
        output = self._search_text(html)
        wrapped = '\n'.join(['\n'.join(textwrap.wrap(x, width=80)) for x in output.split('\n')])

        return re.sub('\n\n+', '\n\n', wrapped).strip()
