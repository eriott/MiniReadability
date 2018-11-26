from lxml import html
from urllib.parse import urlparse

from src.services import ContentDefineService
from src.converters import HtmlToTextConverter


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


class RelativeLinksProcessor:
    def process(self, content, base_url):
        parsed_base_url = urlparse(base_url)
        scheme, host = parsed_base_url.scheme, parsed_base_url.netloc

        for link in content.xpath('.//a'):
            print(link)
            if 'href' in link.attrib:
                parsed = urlparse(link.attrib['href'])
                if (not parsed.scheme) or (not parsed.netloc):
                    path = parsed.path if parsed.path.startswith('/') else '/' + parsed.path
                    fragment = '#' + parsed.fragment if parsed.fragment else ''
                    link.attrib['href'] = '{0}://{1}{2}{3}'.format(scheme, host, path, fragment)