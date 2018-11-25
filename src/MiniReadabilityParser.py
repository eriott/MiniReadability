from lxml import html

from src.ContentDefineService import ContentDefineService
from src.HtmlToTextConverter import HtmlToTextConverter
from src.RelativeLinksProcessor import RelativeLinksProcessor


class MiniReadabilityParser:
    def parse(self, page, url):
        title = ''
        tree = html.fromstring(page)
        content = ContentDefineService().get_content(tree)
        RelativeLinksProcessor().process(content, url)
        if not content.xpath('.//h1'):
            og_titles = tree.xpath('//meta[@property="og:title"]/@content[1]')
            og_title = og_titles[0] + '\n\n' if og_titles else None
            title_tag = tree.xpath('//title')[0].text_content() + '\n\n' if tree.xpath('//title') else ''
            title = og_title or title_tag

        return title + HtmlToTextConverter().convert(content)
