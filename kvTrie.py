class TrieNode:

    
    def __init__(self, char):
        #Instantiate each character with a character
        self.char = char
        #The keys of the dictionary are the characters of the children while the values are their nodes
        #For leafs the key is "" and the value is another trie (root node)
        self.children = {}
        #This is to check if we are at the end of trie key
        self.is_leaf = False
        #The value that is stored (if the node is a leaf node)
        self.value = None
        #If the value has nested data then they are stored in this trie
        self.trie = None

class Trie:

    def __init__(self):

        self.root = TrieNode('')

    def insert(self,key,value):
        #We start from the root
        node = self.root

        #We traverse the trie using each letter of the key
        for char in key:
            if char in node.children:
                node = node.children[char]
            #In case the character does not exist create a new one and add it in the children of the node 
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        node.is_leaf = True 
        node.value = value
        node.trie = Trie()
        #Return the trie of the leaf node
        return node

    def search(self,key):
        #We start from the root
        node = self.root

        #We traverse the trie using each letter of the key
        for char in key:
            if char in node.children:
                node = node.children[char]
            else:
                return

        if node.is_leaf :
            return node

class KV_Trie(Trie):

    def __init__(self):
        self.root = Trie()

    def insert(self,key,value):

        root_node = self.root
        #Insert the key into a trie and create another trie at the end of it
        root = root_node.insert(key,value)
        #There will always be one trie that will store the main keys
        self.rec_insert(key,value,root.trie)


    def rec_insert(self,key,value,root_trie):

        for dict_key,dict_value in value.items():
            #After that in some cases (where there are nested values, additional tries will be created)
            if isinstance(dict_value,dict):
                root = root_trie.insert(dict_key,dict_value)
                self.rec_insert(dict_key,dict_value,root.trie)
            #Otherwise just a simple Trie insert will do
            else:
                root_trie.insert(dict_key,dict_value)

    def search(self,key):
        #We start our search from the root of the main tree
        node = self.root
        split_key = key.split(".",1)
        root = node.search(split_key[0])

        if root is None:
            #print('There is no such main key in the tree!')
            return

        if len(split_key) >=2 and split_key[1]:
            return self.rec_search(split_key[1],root)
        else:
            return root.value

    def rec_search(self,key,root_node):
        split_key = key.split(".",1)
        root_node = root_node.trie.search(split_key[0])
        if root_node is None:
            #print('There is no such secondary key in the tree!')
            return

        if len(split_key) >=2 and split_key[1]:
            return self.rec_search(split_key[1],root_node)
        else:
            return root_node.value

    def delete(self,key):
        #We start our search from the root of the main tree
        node = self.root
        root = node.search(key)
        if root is None:
            #print('There is no such main key in the tree!')
            return False
        root.is_leaf = False
        del root.value 
        del root.trie
        return True