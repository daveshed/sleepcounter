from os import path, listdir

FONT_DIR = path.dirname(path.realpath(__file__))

available_fonts = {}
for file in listdir(FONT_DIR):
    if file.endswith('.ttf'):
        available_fonts[file] = path.join(FONT_DIR, file)
