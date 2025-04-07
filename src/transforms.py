from htmlnode import *
from textnode import *

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    def delimiter_to_text_type_enum(delim):
        match delim:
            case "**":
                return TextType.BOLD
            case "`":
                return TextType.CODE
            case "_":
                return TextType.ITALIC
            case _:
                raise Exception(f"Invalid delimiter {delim}")

    for node in old_nodes:
        if (isinstance(node, HTMLNode) or 
            delimiter not in node.text or 
            node.text_type is not text_type.TEXT):
            new_nodes.append(node)
        elif isinstance(node, TextNode):
            splits = node.text.split(delimiter)
            #if splitting on delimiter give us an odd number of of strings
            if delimiter in node.text and len(splits) % 2 == 1:
                sub_nodes = []
                for index, string in enumerate(splits):

                    if not string.strip():
                        raise Exception(f"Invalid Markdown: empty content detected between delimiters: {node.text}")

                    #odd (outer) list element
                    elif index % 2 == 0:
                        sub_nodes.append(TextNode(string, text_type.TEXT))
                    
                    #even (inner) list element
                    else:
                        sub_nodes.append(TextNode(string, delimiter_to_text_type_enum(delimiter)))

                #add the contents of that list to the new list
                new_nodes.extend(sub_nodes)
        else:
            raise Exception(f"Unsupported node type: {node}")
    return new_nodes