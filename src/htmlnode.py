class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_str = ""
        for key, value in self.props.items():
            props_str = props_str + f" {key}=\"{value}\""
        return props_str
    
    def __repr__(self):
        html = self.props_to_html()
        return f"HTML Node:\n  tag: {self.tag}\n  value: {self.value}\n  props: {self.props}\n===========\nprops html: {html}"
    
properties = {
    "href": "https://www.google.com",
    "target": "_blank",
}

test_node = HTMLNode("a", "this is a link", None, properties)

def main():
    print(test_node)


main()