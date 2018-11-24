import os


class TextFileWriter:
    def write(self, file_path, text):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(text)
