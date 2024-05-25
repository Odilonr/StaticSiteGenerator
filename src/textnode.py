# Text types constants
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

# Block types constants
block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unorded_list = "unorded_list"
block_type_ordered_list = "ordered_list"

from htmlnode import LeafNode,  HTMLNode,   ParentNode
import re

class TextNode:
    """
    Represents a text node with a specific type (e.g., bold, italic, code).
    """
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'

def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode('b', text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode('i', text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode('code', text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode('a',text_node.text, {"href":text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode('img', "", {"src":text_node.url, "alt":text_node.text})
    raise Exception(f'Text node type is not supported: {text_node.text_type}')



def split_nodes_delimiter(old_nodes, delimiter, tex_type):
    """
    Split nodes by a delimiter and assign a new text type to the split parts.
    """
    # Define regex patterns for delimiters
    if delimiter == '*':
        delimiter = r"(?<!\*)\*(?!\*)"
    elif delimiter == '`':
        delimiter = r"`(.*?)`"
    elif delimiter == '**':
        delimiter = r"\*\*(.*?)\*\*"     
    else:
        raise Exception('Invalid markdown Syntax')   

    nodes_split = []
    # Split each old node by the delimiter and create new nodes with the appropriate text type
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            nodes_split.append(old_node)
            continue

        to_add_toNodes_split =[]
        old_node_text_split = re.split(delimiter, old_node.text)

        for i in range(0,len(old_node_text_split)):                
            if (i + 1) % 2 == 0:
                to_add_toNodes_split.append(TextNode(old_node_text_split[i],tex_type))
            else:
                if old_node_text_split[i] != '':    
                    to_add_toNodes_split.append(TextNode(old_node_text_split[i],text_type_text))

        nodes_split.extend(to_add_toNodes_split)
    
    return nodes_split
    


def extract_markdown_images(text):
    return re.findall(r'!\[(.*?)\]\((.*?)\)',text)


def extract_markdown_links(text):
    return re.findall(r'\[(.*?)\]\((.*?)\)',text)

def split_nodes_image(old_nodes):
    nodes_split = []
    for old_node in old_nodes:
        if not old_node.text:
            continue 
        image_tuples_extracted = extract_markdown_images(old_node.text)
        if not image_tuples_extracted:
            nodes_split.append(old_node)
            continue   
        
        for image_tuple in image_tuples_extracted:
            old_node_text = old_node.text.split(f"![{image_tuple[0]}]({image_tuple[1]})", 1)
           
            if old_node_text[0] == '' or old_node_text[0].isspace():
                nodes_split.append(TextNode(image_tuple[0],text_type_image, image_tuple[1]))
                if old_node_text[1] == '' or old_node_text[1].isspace():
                    break
                if not bool(re.search(r"!\[(.*?)\]\((.*?)\)", old_node_text[1])):
                    nodes_split.append(TextNode(old_node_text[1],text_type_text))
                    break
                old_node = TextNode(old_node_text[1],text_type_text)
            else:
                nodes_split.append(TextNode(old_node_text[0],text_type_text))
                nodes_split.append(TextNode(image_tuple[0],text_type_image, image_tuple[1]))
                if old_node_text[1] == '' or old_node_text[1].isspace():
                    break
                if not bool(re.search(r"!\[(.*?)\]\((.*?)\)", old_node_text[1])):
                    nodes_split.append(TextNode(old_node_text[1],text_type_text))
                    break
                old_node = TextNode(old_node_text[1],text_type_text)
               

    return nodes_split
    
def split_nodes_link(old_nodes):
    nodes_split = []
    for old_node in old_nodes:
        if not old_node.text:
            continue 
        links_tuples_extracted = extract_markdown_links(old_node.text)
        if not links_tuples_extracted:
            nodes_split.append(old_node)
            continue   

        for link_tuple in links_tuples_extracted:
            old_node_text = old_node.text.split(f"[{link_tuple[0]}]({link_tuple[1]})", 1)

            if old_node_text[0] == '' or old_node_text[0].isspace():
                nodes_split.append(TextNode(link_tuple[0],text_type_link, link_tuple[1]))
                if old_node_text[1] == '' or old_node_text[1].isspace():
                    break
                if not bool(re.search(r"\[(.*?)\]\((.*?)\)", old_node_text[1])):
                    nodes_split.append(TextNode(old_node_text[1],text_type_text))
                    break
                old_node = TextNode(old_node_text[1],text_type_text)
            else:
                nodes_split.append(TextNode(old_node_text[0],text_type_text))
                nodes_split.append(TextNode(link_tuple[0],text_type_link, link_tuple[1]))
                if old_node_text[1] == '' or old_node_text[1].isspace():
                    break
                if not bool(re.search(r"\[(.*?)\]\((.*?)\)", old_node_text[1])):
                    nodes_split.append(TextNode(old_node_text[1],text_type_text))
                    break
                old_node = TextNode(old_node_text[1],text_type_text)

    return nodes_split

def text_to_texnode(text):
    node = TextNode(text, text_type_text)
   

    node_split_bold = split_nodes_delimiter([node], '**', text_type_bold)
    node_split_code = split_nodes_delimiter(node_split_bold, '`', text_type_code)
    node_split_italic = split_nodes_delimiter(node_split_code, '*', text_type_italic)
    node_split_image = split_nodes_image(node_split_italic)
    node_split_links = split_nodes_link(node_split_image)

    return node_split_links

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    remove_whitespace = lambda x: x.strip(' ')
    remove_empty_blocks = lambda x: x != ''

    blocks = list(filter(remove_empty_blocks, blocks))

    for i, block in enumerate(blocks):
        if '\n' in block:
            temp_block = block.split('\n')
            temp_block = list(map(remove_whitespace,temp_block))
            blocks[i] = '\n'.join(temp_block)
        else:
            blocks[i] = remove_whitespace(block)

    blocks = list(filter(remove_empty_blocks, blocks))
    
    return blocks

def block_to_block_type(block):
    if bool(re.match(r"(#{1,6})\s(?!\s)(.+)", block)):
        return block_type_heading
    
    if block.startswith('```') and block.endswith('```'):
        return block_type_code
    
    block_list = block.split('\n')
    quote_in_all = True
    for line in block_list:
        if not line.startswith('>'):
            quote_in_all = False
            break
    if quote_in_all:
        return block_type_quote
    
    unordered_list = True
    for line in block_list:
        if not (line.startswith('* ') or line.startswith('- ')):
            unordered_list = False
            break
    if unordered_list:
        return block_type_unorded_list
    
    ordered_list = True
    for i, block in enumerate(block_list):
        if not(block.startswith(f'{i+1}. ')):
            ordered_list = False
    if ordered_list:
        return block_type_ordered_list
    
    return block_type_paragraph

def add_children(block):
    children = []
    text_nodes = text_to_texnode(block)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def block_to_html_node_paragraph(block):
    return ParentNode(tag="p",children = add_children(block))

def block_to_html_node_blockquote(block):
    return ParentNode(tag="blockquote",children=add_children(block))

def block_to_html_node_heading(block):
    if bool(re.match(r"(#)\s(?!\s)(.+)", block)):
        return ParentNode(tag="h1",children=add_children(block.replace("# ","",1)))
    
    if bool(re.match(r"(##)\s(?!\s)(.+)", block)):
        return ParentNode(tag="h2",children=add_children(block.replace("## ","",1)))
    
    if bool(re.match(r"(###)\s(?!\s)(.+)", block)):
        block = re.sub(r"(###)\s(?!\s)", "", block)
        return ParentNode(tag="h3",children=add_children(block.replace("### ","",1)))
    
    if bool(re.match(r"(####)\s(?!\s)(.+)", block)):
        block = re.sub(r"(####)\s(?!\s)", "", block)
        return ParentNode(tag="h4",children=add_children(block.replace("#### ","",1)))
    
    if bool(re.match(r"(#####)\s(?!\s)(.+)", block)):
        block = re.sub(r"(#####)\s(?!\s)", "", block)
        return ParentNode(tag="h5",children=add_children(block.replace("##### ","",1)))
    
    if bool(re.match(r"(######)\s(?!\s)(.+)", block)):
        block = re.sub(r"(######)\s(?!\s)(.+)", "", block)
        return ParentNode(tag="h6",children=add_children(block.replace("###### ","",1)))
    

def block_to_html_node_code(block):
    node = ParentNode(tag="code",children=add_children(block))
    return ParentNode(tag="pre", children=[node])

def block_to_html_node_ordered_list(block):
    items = block.split('\n')
    children = []
    for i, item in enumerate(items):
        item = item.replace(f"{i+1}. ","")
        children.append(ParentNode(tag="li",children=add_children(item)))
    return ParentNode(tag ="ol", children=children)

def block_to_html_node_unordered_list(block):
    items = block.split("\n")
    children = []
    for item in items:
        if item.startswith('* '):
            item = item.replace(f"* ", "")
            children.append(ParentNode(tag="li",children=add_children(item)))
        else:
            item = item.replace(f"- ", "")
            children.append(ParentNode(tag="li", children=add_children(item)))
    return ParentNode(tag="ul",children=children)
      
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        type_of_block = block_to_block_type(block)

        if type_of_block == block_type_paragraph:
            children.append(block_to_html_node_paragraph(block))
        if type_of_block == block_type_quote:
            children.append(block_to_html_node_blockquote(block))
        if type_of_block == block_type_heading:
            children.append(block_to_html_node_heading(block))
        if type_of_block == block_type_code:
            children.append(block_to_html_node_code(block))
        if type_of_block == block_type_ordered_list:
            children.append(block_to_html_node_ordered_list(block))
        if type_of_block == block_type_unorded_list:
            children.append(block_to_html_node_unordered_list(block))
        

    return ParentNode(tag="div", children=children)

    
   

    

            


    

            