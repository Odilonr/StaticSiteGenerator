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
                      block_to_block_type,
                      markdown_to_html_node)

from htmlnode import HTMLNode,ParentNode,LeafNode
import os
import shutil


def main():
   text = """        This is **bolded** paragraph\n\n\n\n    This is another paragraph with *italic* text and `code` here\n This is the same paragraph on a new line\n\n* This is a list\n* with items \n\n1. Get strong\n2. Believe in God\n\n### Heading 1\n\n# Last one I promise"""
   source = "src"
   print(os.listdir(os.path.join(os.getcwd(),source)))
   copy_directory_content("src", "test")
def delete_folder_content(file_path):
   for entry in os.listdir(file_path):
      path = os.path.join(file_path,entry)
      if os.path.isfile(path) or os.path.islink(path):
         os.unlink(path)
      else:
         shutil.rmtree(path)

def copy_directory_content(source, destination):
   cwd = os.getcwd()
   source_path = os.path.join(cwd, source)
   destination_path = os.path.join(cwd, destination)
   if os.path.exists(destination_path):
      delete_folder_content(destination_path)
   entries = os.listdir(source_path)
   for entry in entries:
      if os.path.isfile(entry):
         shutil.copy(os.path.join(source_path,entry), destination_path)
      else:
         os.mkdir(os.path.join(destination_path,entry))
         copy_directory_content(os.path.join(source, entry), os.path.join(destination, entry))



  




main()