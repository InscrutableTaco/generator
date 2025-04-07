from textnode import *

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)

        self.value = value
        # A string representing the value of the HTML tag (e.g. the text inside a paragraph)

        self.children = [] if children is None else children
        # A list of HTMLNode objects representing the children of this node

        self.props = {} if props is None else props
        # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}


    def to_html(self):
        raise NotImplementedError("not implemented")
    
    def props_to_html(self):
        props_str = ""
        for key, value in self.props.items():
            props_str = props_str + f" {key}=\"{value}\""
        return props_str
    
    def children_to_html(self):
        return "".join([child.to_html() for child in self.children])
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and 
                self.value == other.value and 
                self.children == other.children and 
                self.props == other.props)
    
    def __repr__(self):
        html = self.props_to_html()
        children = self.children_to_html()
        return f"HTML Node:\n  tag: {self.tag}\n  value: {self.value}\n  children: {children}\n  props: {html}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a non-null value.")
        if not self.tag:
            open, close = "", ""
        else:
            open, close = f"<{self.tag}{self.props_to_html()}>", f"</{self.tag}>"
        return f"{open}{self.value}{close}"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("parent node missing a tag")
        elif self.children is None:
            raise ValueError("child node(s) missing")
        elif len(self.children) == 0:
            raise ValueError("ParentNode must have at least one child")
        else:
            open, close = f"<{self.tag}{self.props_to_html()}>", f"</{self.tag}>"
            return f"{open}{self.children_to_html()}{close}"
        
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid text node text type")