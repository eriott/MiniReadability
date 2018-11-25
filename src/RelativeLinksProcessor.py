from urllib.parse import urlparse


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
