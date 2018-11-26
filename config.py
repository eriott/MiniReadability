max_line_width = 80

container_tags = ['div', 'article', 'section']
ignore_tags = ['script', 'style', 'footer', 'nav', 'form']
text_tags = ['h[1-6]', 'p', 'ul', 'ol', 'li', 'b', 'i', 'pre', 'code', 'a', 'br', 'code']
not_format_tags = ['code']

format_rules = {
    'p': '\n\n{val}\n\n',
    'h[1-6]': '\n\n{val}\n\n',
    'a': lambda params: '{val} [{href}]' if 'href' in params else '{val}',
    'li': ' - {val}\n',
    'ul': '\n{val}\n',
    'ol': '\n{val}\n',
    'br': '\n'
}