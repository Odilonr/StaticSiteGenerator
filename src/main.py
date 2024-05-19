from textnode import (TextNode,
                      text_type_bold,
                      text_type_code,
                      text_type_image,
                      text_type_italic,
                      text_type_link,
                      text_type_text,
                      text_node_to_html_node,
                      split_nodes_delimiter, 
                      split_nodes_image,
                      split_nodes_link,
                      text_to_texnode,
                      markdown_to_blocks,
                      block_to_block_type)

from htmlnode import HTMLNode,ParentNode,LeafNode


def main():
   text = """        This is **bolded** paragraph\n\n\n\n    This is another paragraph with *italic* text and `code` here\n This is the same paragraph on a new line\n\n * This is a list\n* with items \n\n1. Get strong\n2. Believe in God\n\n### Heading 1\n\n# Last one I promise"""
   print(text)
   changed = markdown_to_blocks(text)
   print(changed)
   print('\n\n'.join(changed))
   print
   for element in changed:
      print(block_to_block_type(element))

  




main()