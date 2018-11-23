class TextFileWriter:
    def write(self, filename, text):
        with open(filename, 'w', encoding='utf-8') as output_file:
            output_file.write(text)