from lxml import html

from src.ContentDefineService import ContentDefineService
from src.HtmlToTextConverter import HtmlToTextConverter


class MiniReadabilityParser:
    def parse(self, content):
        tree = html.fromstring(content)
        content = ContentDefineService().get_content(tree)
        return HtmlToTextConverter().convert(content)
