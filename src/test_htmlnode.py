import unittest

from htmlnode import HTMLNode,LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        htmlnode = HTMLNode(tag='p', value='once upon a time',children=None,
                            props={"href": "https://www.google.com", "target": "_blank"})
        excepted = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(htmlnode.props_to_html(), excepted)

    def test_to_html_no_children(self):
        leafNode = LeafNode("p", "This is a paragraph of text.")
        excepted = '<p>This is a paragraph of text.</p>'
        self.assertEqual(leafNode.to_html(), excepted)
    
    def test_to_html_with_children_props(self):
        leafNode = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        excepted = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(leafNode.to_html(), excepted)

    def test_to_html_no_tag(self):
        leafNode = LeafNode(None, 'Man, this is good')
        excepted = 'Man, this is good'
        self.assertEqual(leafNode.to_html(), excepted)

    def test_to_html_with_children(self):
        child_node = LeafNode("span",'child')
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode('b','grandchild')
        child_node = ParentNode('span',[grandchild_node])
        parent_node = ParentNode('div',[child_node])
        self.assertEqual(parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",)

    def test_to_html_with_many_children(self):
        parentNode = ParentNode(tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(parentNode.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

    


