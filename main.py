import sys

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def height_get(self, root):
        return root.height if root else 0
    
    def balance_get(self, root):
        return self.height_get(root.left) - self.height_get(root.right) if root else 0
    
    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.height_get(y.left), self.height_get(y.right))
        x.height = 1 + max(self.height_get(x.left), self.height_get(x.right))
        return x
    
    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x 
        x.right = T2
        x.height = 1 + max(self.height_get(x.left), self.height_get(x.right))
        y.height = 1 + max(self.height_get(y.left), self.height_get(y.right))
        return y
    
    def insert(self, root, key):
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            return root
        
        root.height = 1 + max(self.height_get(root.left), self.height_get(root.right))
        balance = self.balance_get(root)

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        
        return root
    
    def min_node_value(self, node):
        while node.left:
            node = node.left
        return node
    
    def max_node_value(self, node):
        while node.right:
            node = node.right
        return node
    
    def delete(self, root, key):
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left and not root.right:
                return None
            elif not root.left:
                return root.right
            elif not root.right:
                return root.left
            temp = self.max_node_value(root.left)
            root.key = temp.key
            root.left = self.delete(root.left, temp.key)

        root.height = 1 + max(self.height_get(root.left), self.height_get(root.right))
        balance = self.balance_get(root)
        
        if balance > 1 and self.balance_get(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.balance_get(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.balance_get(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.balance_get(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        
        return root
    
    def preorder(self, root):
        return [] if not root else [root.key] + self.preorder(root.left) + self.preorder(root.right)
    def inorder(self, root):
        return [] if not root else self.inorder(root.left) + [root.key] + self.inorder(root.right)
    def postorder(self, root):
        return [] if not root else self.postorder(root.left) + self.postorder(root.right) + [root.key] 
    
if __name__ == "__main__":
    moves = sys.stdin.readline().strip().split()
    tree = AVLTree()
    root = None
    for move in moves[:-1]:
        if move[0] == "A":
            root = tree.insert(root, int(move[1:]))
        elif move [0] == "D":
            root = tree.delete(root, int(move[1:]))

    final = moves[-1]
    if not root:
        print("EMPTY")
    else:
        if final == "PRE":
            print(" ".join(map(str, tree.preorder(root))))
        elif final == "IN":
            print(" ".join(map(str, tree.inorder(root))))
        elif final == "POST":
            print(" ".join(map(str, tree.postorder(root))))