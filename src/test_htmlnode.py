import unittest

from htmlnode import *
from textnode import *
from transforms import *

'''
The HTMLNode class should have 4 data members set in the constructor:

tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
children - A list of HTMLNode objects representing the children of this node
props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
'''

class TestHTMLNode(unittest.TestCase):
    
    def test_eq(self):
        node = HTMLNode("h1", "this is a header", [], {})
        node2 = HTMLNode("h1", "this is a header", [], {})
        self.assertEqual(node, node2)

    def test_diff_textvalue(self):
        node = HTMLNode("h1", "this is a header", [], {})
        node2 = HTMLNode("h1", "this is a different header", [], {})
        self.assertNotEqual(node, node2)

    def test_diff_children(self):
        node = HTMLNode("p", "this is a paragraph", [], {})
        node2 = HTMLNode("p", "this is a paragraph", [node], {})
        self.assertNotEqual(node, node2)

    def test_link_att(self):
        node = HTMLNode("a", "this is a link", [], {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "this is a link", [], {"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")




    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_great_grandchildren(self):
        great_grandchild_node = LeafNode("b", "grandchild")
        grandchild_node = ParentNode("h1", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><h1><b>grandchild</b></h1></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")



if __name__ == "__main__":
    unittest.main()
    