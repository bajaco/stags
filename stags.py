import requests
from treeify import Tree
from helpers import attributes_pairs
class Element:
    def __init__(self, name='', contents='', attributes='{}'):
        self.name = name
        self.contents = contents
        self.attributes = attributes
    
    def __repr__(self):
        return self.name

    def get_attribute(self, attribute):
        if attribute in self.attributes:
            return self.attributes[attribute]
        else:
            return None

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
        in_quote = False
        contents = ''
        
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
                        contents += c
                #in tag
                else:
                    if c == '>':
                        self.tags.append((tag_name,i,contents))
                        tag_name = ''
                        contents = ''
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
        contents = ''
        for tag in self.tags:
            parts = tag[0].split()
            name = tag[0]
            attributes = {}
            if len(parts) > 1:
                name = parts[0]
                attributes = attributes_pairs(''.join(parts[1:])) 
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
                        self.tree.node.contents += tag[2]
                        self.tree.get_parent()
                    else:
                        self.tree.birth(Element(name, '', attributes))
        self.query_list = self.tree.list

    # Function to display original text between tag
    # indices. It works similarly to string slicing.
    def between(self, a, b):
        return self.text[self.tags[a][1]
                - len(self.tags[a][0]) - 1:
                self.tags[b-1][1]+1]

    def reset_query(self):
        self.query_list = self.tree.list
    
    def query(self):
        return self.query_list

    def filter_attributes(self, query):
        self.query_list = [e for e in self.query_list if query in e.attributes]

    def filter_tags(self, query):
        self.query_list = [e for e in self.query_list if e.name == query]

    def ascend(self):
        self.query_list = [e.parent for e in self.query_list if e.parent is not None]
   
    def descend(self):
        res = []
        for e in self.query_list:
            for c in e.children:
                res.append(c)
        self.query_list = res

    def dump(self):
        self.tree.dump()
    

