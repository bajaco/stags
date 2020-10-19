import requests

# The node class get's attributes from the
# core object, allowing trees to be built 
# from any object type
class Node:
    def __init__(self, obj):
        self.core = obj
        self.parent = None
        self.children = []

    def __repr__(self):
        return self.core.__repr__()

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self.core, attr)

class Tree:
    def __init__(self, obj):
        self.node = Node(obj)

    def has_parent(self):
        if self.node.parent:
            return True
        return False

    def has_children(self):
        return len(self.node.children)
        
    def get_parent(self):
        self.node = self.node.parent

    def get_child(self,index):
        self.node = self.node.children[index]
    
    def get_children(self):
        return self.node.children

    def birth(self, obj):
        child = Node(obj)
        self.node.children.append(child)
        child.parent = self.node
        self.node = child

    def get_root(self):
        while self.has_parent():
            self.get_parent()
    
    # Dump all nodes for testing purposes
    def dump(self):
        print(str(self.node.parent) + '->' + str(self.node))
        if self.has_children():
            for child in self.get_children():
                self.node = child
                self.dump()

class Element:
    def __init__(self, name='', content='', attributes='{}'):
        self.name = name
        self.content = content
        self.attributes = attributes
    
    def __repr__(self):
        return self.name

class Stags:
    def __init__(self,url,agent,method):
        self.user_agent = {'User-Agent': agent}
        self.method = method
        if self.method.lower() == 'get':
            self.text = requests.get(url, 
                    headers = self.user_agent).text
        self.tree = Tree(Element('root'))
        
        # Initialization for parsing
        self.tags = []
        tag_name = ''
        in_tag = False
        in_comment = False
        content = ''
        
        # Parse text into tags
        for i,c in enumerate(self.text):
            if not in_comment:
                if not in_tag:
                    if c == '<':
                        #scripts are ignored as well as comments
                        if (self.text[i:i+4] == '<!--'
                                or self.text[i:i+7] == '<script'):
                            in_comment = True
                        else:
                            in_tag = True
                    else:
                        content += c
                #in tag
                else:
                    if c == '>':
                        self.tags.append((tag_name,i,content))
                        tag_name = ''
                        content = ''
                        in_tag = False
                    else:
                        tag_name += c
            else:
                if c == '>':
                    if (self.text[i-2:i+1] == '-->'
                            or self.text[i-7:i+1] == '/script>'):
                        in_comment = False
        
        # Generate list of duplicates to prevent faulty
        # tags from being parent elements
        self.duplicates = []
        for t in self.tags:
            if len(t[0]):
                if t[0][-1] != '/':
                    self.duplicates.append(t[0])

        for t in self.tags:
            if ('/' + t[0] in self.duplicates and
                    t[0] in self.duplicates):
                self.duplicates.remove('/' + t[0])
                self.duplicates.remove(t[0])

        for t in self.tags:
            if ' ' in t[0]:
                if ('/' + t[0].split()[0] in self.duplicates and
                        t[0] in self.duplicates):
                    self.duplicates.remove('/' + t[0].split()[0])
                    self.duplicates.remove(t[0])
        
        # Iterate tags and build tree
        content = ''
        for tag in self.tags:
            parts = tag[0].split()
            name = tag[0]
            attributes = {}
            if len(parts) > 1:
                name = parts[0]
                for part in parts[1:]:
                    if '=' in part:
                        dict_parts = part.split('=')
                        key = dict_parts[0]
                        value = dict_parts[1][1:-1]
                        attributes[key] = value

            if tag[0] in self.duplicates:
                self.duplicates.remove(tag[0])
                self.tree.birth(Element(name,'',attributes))
                self.tree.get_parent()
            else:
                if len(tag[0]):
                    if tag[0][-1] == '/':
                        self.tree.birth(Element(name, '', attributes))
                        self.tree.get_parent()
                    elif tag[0][0] == '/':
                        self.tree.node.content += tag[2]
                        self.tree.get_parent()
                    else:
                        self.tree.birth(Element(name, '', attributes))
        
        self.tree.get_root()
        self.tree.dump()

    # Function to display original text between tag
    # indices. It works similarly to string slicing.
    def between(self, a, b):
        return self.text[self.tags[a][1]
                - len(self.tags[a][0]) - 1:
                self.tags[b-1][1]+1]
    

url = 'https://www.duckduckgo.com'
agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'
stags = Stags(url, agent, 'get')


