import os


class TextFileWriter:
    def write(self, file_path, text):
        try:
            directory = os.path.dirname(file_path)
            if directory:
                if not os.path.exists(directory):
                    os.makedirs(directory)

            with open(file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(text)

            print('File saved {0}'.format(file_path))
        except Exception as e:
            print('Can not save file {0} with error {1}'.format(file_path, e))