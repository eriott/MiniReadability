max_line_width = 80

ignore_tags = ['script', 'style']

text_tags = ['h[1-6]', 'p', 'ul', 'li', 'b', 'i', 'pre', 'code', 'a']

container_tags = ['div', 'article', 'section']

format_rules = {
    'p': '\n\n{val}\n\n',
    'h[1-6]': '\n\n{val}\n\n',
    'a': lambda params: '{val} [{href}]' if 'href' in params else '{val}',
    'li': ' - {val}\n',
    'ul': '\n{val}\n'
}