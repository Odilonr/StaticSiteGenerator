class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError('Not yet implemented')

    def props_to_html(self):
        if self.props is None:
            return ""
        string_repr = []
        for attribute in self.props:
            string_repr.append(f'{attribute}="{self.props[attribute]}"')
        return ' '.join(string_repr)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError('Leaf Nodes require a value')
        if self.tag is None:
            return f'{self.value}'
        if self.props is None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        
        return f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag,children, props=None):
        super().__init__(tag,None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('Tag Not provided')
        if self.children is None:
            raise ValueError('What type of parent has no children')

        child_html = ""

        for children in self.children:
            child_html += children.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"



