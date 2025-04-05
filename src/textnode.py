from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

#    def __str__(self):
#        return f"TextNode() with the properties:\n  text: \"{self.text}\"\n  type: {self.text_type.value}\n  url: {self.url}"

    def __eq__(self, textnode):
        if self.text == textnode.text and self.text_type == textnode.text_type and self.url == textnode.url:
            return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
