def load(file_name):
    with open(f'language/{file_name}') as f:
        try:
            return eval(f.read())
        except UnicodeDecodeError:
            with open(f'language/{file_name}',encoding='utf-8') as f:

                return eval(f.read())

