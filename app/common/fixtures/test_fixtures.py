import os
from PIL import Image


def html_wiki_example_game_engines():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "html_wiki_example_game_engines.html"
    )
    txt = open(file_path).read()
    return txt


def wiki_btn_image():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "wikimedia_button.png"
    )
    return Image.open(file_path)
