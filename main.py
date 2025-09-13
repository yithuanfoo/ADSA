import sys

# Defining class called Node which is needed to store each element in an AVL tree
class Node:
    def __init__(self, key):    # Constructor which runs when new node is created
        self.key = key  # Stores the actual data in the node
        self.left = None    # Initialises the left child of the node
        self.right = None   # Initialises the right child of the node
        self.height = 1 # Initialises the height of the node, which always start with 1

# Defining class called AVLTree
class AVLTree:
    def height_get(self, root): # Helper function which returns the height of a node
        if root:    # If root is not None, returns actual store height
            return root.height
        else:   # If root is None, returns 0
            return 0
    
    def balance_get(self, root):    # Helper function which calculates the balance factor of a node
        if root:    # If root is not None, calculate balance factor
            return self.height_get(root.left) - self.height_get(root.right) # Subtracts the height of the left subtree with the height of the right subtree
        else:   # If root is None, returns 0
            return 0
    
    def right_rotate(self, y):  # Function which does a right rotation
        x = y.left  # y is the unbalanced node, x is y's left child, which will be moved up to become the new root of the subtree
        temp_subtree = x.right  # Before rotating, save x's right child as rotating will change the child
        x.right = y # Make y the right child of x
        y.left = temp_subtree   # The original right child of x is now the left child of y
        y.height = 1 + max(self.height_get(y.left), self.height_get(y.right))   # Update the height of y as its children may have changed
        x.height = 1 + max(self.height_get(x.left), self.height_get(x.right))   # Update the height of x which is the new root of this subtree
        return x
    
    def left_rotate(self, x): # Function which does a left rotation
        y = x.right # x is the unbalanced node, y is x's right child, which will be moved up to become the new root of this subtree
        temp_subtree = y.left   # Before rotating, y's left child as rotating will change the chiod
        y.left = x  # Make x the left child of y
        x.right = temp_subtree  # The original left child of y is now the right child of x
        x.height = 1 + max(self.height_get(x.left), self.height_get(x.right))   # Update the height of x as it is now lower in the tree
        y.height = 1 + max(self.height_get(y.left), self.height_get(y.right))   # Update the height of y which is the new root of this subtree
        return y
    
    def insert(self, root, key):    # Function which insert a node into the AVL Tree (recursive function)
        if not root:    # If the current root is None, create a new node (base case)
            return Node(key)
        elif key < root.key:    # If the new value is smaller, go down the left subtree recursively
            root.left = self.insert(root.left, key)
        elif key > root.key:    # If the new value is bigger, go down the right subtree recursively
            root.right = self.insert(root.right, key)
        else:   # If the value is equal to the current node's value, don't do anything
            return root
        
        root.height = 1 + max(self.height_get(root.left), self.height_get(root.right))  # After a node has been inserted, go back to the top and update the node's height
        balance = self.balance_get(root)    # Calculate the balance factor (If -1, 0, +1 -> balanced, if < -1 -> right heavy, if > +1 -> left heavy)

        # Balancing the tree
        # Taking into account the different combination of balance factors, rotate the tree to make it balanced again
        if balance > 1 and key < root.left.key: # If the tree is left heavy, and the value was inserted into the left subtree of the left child, fix it with a single right rotation
            return self.right_rotate(root)
        if balance < -1 and key > root.right.key:   # If the tree is right heavy and the value was inserted into the right subtree of the right child, fix it with a single left rotation
            return self.left_rotate(root)
        if balance > 1 and key > root.left.key: # If the tree is left heavy and the value was inserted into the right subtree of the left child, fix it with two rotations, first with a left rotate of the left child and then a right rotate at the root
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and key < root.right.key:   # If the tree is right heavy and the value was inserted into the left subtree of the right child, fix it with two rotations, first with a right rotate of the right child and then a left rotate at the root
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        
        return root

    def max_node_value(self, node): # Helper function for the delete function, finds the maximum value node in a subtree (always the right most node)
        while node.right:   # This keeps going as long as the current node has a right child
            node = node.right   # Once a node is reach with no right child, that is the maximum value node
        return node
    
    def delete(self, root, key):    # Function which deletes a node from the AVL Tree (recursive function)
        if not root:    # If current root is None, there is nothing to delete so return root ( base case )
            return root
        elif key < root.key:    # If the value to delete is smaller, go down the left subtree recursively
            root.left = self.delete(root.left, key)
        elif key > root.key:    # If the value to delete is bigger, go down the right subtree recursively
            root.right = self.delete(root.right, key)
        else:   # If the node has been found and the node has no children, just delete the node
            if not root.left and not root.right:
                return None
            elif not root.left: # If the node has a right child, replace the node with its right child
                return root.right
            elif not root.right:    # If the node has a left child, replace the node with its left child
                return root.left
            temp = self.max_node_value(root.left)   # If the node has two children, find the largest value in the left subtree and store in a temporary variable
            root.key = temp.key # Copy the value into the current node
            root.left = self.delete(root.left, temp.key)    # Delete the largest node from the left subtree

        root.height = 1 + max(self.height_get(root.left), self.height_get(root.right))  # After a node has been deleted, update the height of the current node as its children may have changed
        balance = self.balance_get(root)    # Calculate the balance factor
        
        if balance > 1 and self.balance_get(root.left) >= 0:    # If the node is left heavy and the left child is also left heavy or balanced, fix it with a single right rotation
            return self.right_rotate(root)
        if balance > 1 and self.balance_get(root.left) < 0: # If the node is left heavy but the left child is right heavy, fix it with two rotations, first with a left rotate of the left child and then a right rotate at the root
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.balance_get(root.right) <= 0:  # If the node is right heavy and the right child is also right heavy or balanced, fix it with a single left rotation
            return self.left_rotate(root)
        if balance < -1 and self.balance_get(root.right) > 0:   # If the node is right heavy but its right child is left heavy, fix it with two rotations, first right rotate the right child and then a left rotation at the root
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        
        return root
    
    # Function for traversing the tree when printing
    def preorder(self, root):   # Preorder traversal (Root -> Left -> Right)
        if not root:    # If current node is None, return an empty list
            return []
        result = [] # Initialise empty list
        result.append(root.key) # Visit the root first
        result += self.preorder(root.left)  # Traverse the left subtree
        result += self.preorder(root.right) # Traverse the right subtree
        return result
    def inorder(self, root):    # Inorder traversal (Left -> Root -> Right)
        if not root:
            return []
        result = []
        result += self.inorder(root.left)   # Traverse the left subtree first
        result.append(root.key) # Visit the root
        result += self.inorder(root.right)  # Traverse the right subtree
        return result
    def postorder(self, root):  # Postorder traversal (Left -> Right -> Root)
        if not root:
            return []
        result = []
        result += self.postorder(root.left) # Traverse the left subtree right
        result += self.postorder(root.right)    # Traverse the right subtree
        result.append(root.key) # Visit the root
        return result

# Main code
if __name__ == "__main__":
    values = sys.stdin.readline().strip().split()    # Reads one line of input from standard input and removes any leading or trailing space and breaks the line into a list of strings seperated by spaces
    tree = AVLTree()    # Initialises a AVL tree
    root = None # Starts with an empty tree
    for value in values[:-1]:   # Loops through all values except the last one as the last one is the traversal order
        if value[0] == "A": # If A, insert that number into the AVL tree
            root = tree.insert(root, int(value[1:]))
        elif value [0] == "D":  # If D, delete that number from the AVL tree
            root = tree.delete(root, int(value[1:]))

    traverse_order = values[-1]    # final value is stored in final_value, which tells us how to traverse the tree
    if not root:    # If root is None, tree is empty and prints EMPTY
        print("EMPTY")
    else:
        if traverse_order == "PRE": # If PRE, traverse the tree using preorder traversal
            print(" ".join(map(str, tree.preorder(root))))
        elif traverse_order == "IN":    # If IN, traverse the tree using inorder traversal
            print(" ".join(map(str, tree.inorder(root))))
        elif traverse_order == "POST":  # If POST, traverse the tree using POST traversal
            print(" ".join(map(str, tree.postorder(root))))