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
        self.root = self.node
        self.list = []
        self.list.append(self.node)

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
        self.list.append(self.node)

    def get_root(self):
        self.node = self.root

    def get_list(self):
        return self.list
    
    # Dump all nodes for testing purposes
    def dump(self):
        print(str(self.node.parent) + '->' + str(self.node))
        if self.has_children():
            for child in self.get_children():
                self.node = child
                self.dump()


