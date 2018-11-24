from urllib.parse import urlparse


class UrlFilepathParser:
    def parse(self, url):
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
