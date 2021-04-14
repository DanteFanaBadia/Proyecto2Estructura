
class Node:
    def __init__(self, data):
        self.key = data
        self.left = None
        self.right = None


def insert(node, key):
    if node is None:
        node = Node(key)
    elif node.key > key:
        node.left = insert(node.left, key)
    elif node.key < key:
        node.right = insert(node.right, key)
    return node


def distance_from_root(node, x):
    if node.key == x:
        return 0
    elif node.key > x:
        return 1 + distance_from_root(node.left, x)
    return 1 + distance_from_root(node.right, x)


def distance_between_2(root, node1, node2):
    if root is None:
        return 0

    if root.key > node1 and root.key > node2:
        return distance_between_2(root.left, node1, node2)

    if root.key < node1 and root.key < node2:  # same path
        return distance_between_2(root.right, node1, node2)

    if node1 <= root.key <= node2:
        return distance_from_root(root, node1) + distance_from_root(root, node2)


def find_dist_wrapper(root, node1, node2):
    if node1 > node2:
        node1, node2 = node2, node1
    return distance_between_2(root, node1, node2)


# Driver code
if __name__ == '__main__':
    root = None
    root = insert(root, 20)
    insert(root, 10)
    insert(root, 5)
    insert(root, 15)
    insert(root, 30)
    insert(root, 25)
    insert(root, 35)
    a, b = 5, 55
    print(find_dist_wrapper(root, 5, 35))

    # This code is contributed by PranchalK