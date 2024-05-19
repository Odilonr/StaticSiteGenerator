import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_texnode,
    markdown_to_blocks)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("a text node", text_type_bold)
        node2 = TextNode("a text node", text_type_bold)
        self.assertEqual(node, node2)
    
    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", text_type_italic, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)",repr(node)
        )

    def test_split_node_delimiter(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        excepted = [
                        TextNode("This is text with a ", text_type_text),
                        TextNode("bolded", text_type_bold),
                        TextNode(" word", text_type_text),
                    ]
        self.assertEqual(new_nodes, excepted)

    def test_extract_links(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        text2 = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"

        self.assertListEqual(extract_markdown_images(text),[("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])
        self.assertListEqual(extract_markdown_links(text2), [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])
        
    def test_split_image_nodes(self):
        node = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        excepted = [
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                ),
            ]
        self.assertListEqual(new_nodes, excepted)

    def test_split_links_nodes(self):
        node = TextNode(
            "[link](https://www.example.com)This is text with an [link2](https://www.example.com) and another [link](https://www.google.com)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        excepted = [
                TextNode("link", text_type_link, "https://www.example.com"),
                TextNode("This is text with an ", text_type_text),
                TextNode("link2", text_type_link, "https://www.example.com"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "link", text_type_link, "https://www.google.com"
                ),
            ]
        self.assertListEqual(new_nodes, excepted)

    def test_text_to_textnode(self):
        text = """This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)
            """
        excepted = [
                    TextNode("This is ", text_type_text),
                    TextNode("text", text_type_bold),
                    TextNode(" with an ", text_type_text),
                    TextNode("italic", text_type_italic),
                    TextNode(" word and a ", text_type_text),
                    TextNode("code block", text_type_code),
                    TextNode(" and an ", text_type_text),
                    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and a ", text_type_text),
                    TextNode("link", text_type_link, "https://boot.dev"),
                ]
        self.assertEqual(text_to_texnode(text), excepted)

    def test_markdown_to_block(self):
        text = """           This is **bolded** paragraph\n\n\n\n    This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n     * with items"""
        excepted = ["This is **bolded** paragraph","This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line","* This is a list\n* with items"]

        self.assertEqual(markdown_to_blocks(text),excepted)




    

if __name__ == "__main__":
    unittest.main()