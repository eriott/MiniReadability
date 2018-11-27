max_line_width = 80

container_tags = ['div', 'article', 'section'] # в этих тегах будет выполняться поиск контента
ignore_tags = ['script', 'style', 'footer', 'nav', 'form']
not_format_tags = ['code'] # содержимое этих тегов не будет форматироваться

format_rules = {
    'p': '\n\n{val}\n\n',
    'h[1-6]': '\n\n{val}\n\n',
    'a': lambda params: '{val} [{href}]' if 'href' in params else '{val}',
    'li': ' - {val}\n',
    'ul': '\n{val}\n',
    'ol': '\n{val}\n',
    'br': '\n'
}