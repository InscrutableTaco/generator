import unittest

from htmlnode import HTMLNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("This is an html node", TextType.BOLD)
        node2 = HTMLNode("This is an html node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_texttype(self):
        node = HTMLNode("This is an html node", TextType.BOLD)
        node2 = HTMLNode("This is an html node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_missing_link(self):
        node = HTMLNode("This is a link node", TextType.LINK, "www.xkcd.com")
        node2 = HTMLNode("This is a link node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_empty_str(self):
        node = HTMLNode("", TextType.BOLD)
        node2 = HTMLNode("This is an html node", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()