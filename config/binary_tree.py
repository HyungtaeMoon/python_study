# binary_tree.py
class TreeNode:
    def __init__(self):
        self.__data = None
        self.__left = None
        self.__right = None

    # 노드 삭제를 확인하기 위한 소멸자
    # 객체가 삭제되기 전에 호출된다
    def __del__(self):
        print("TreeNode of {} is deleted".format(self.data))

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, left):
        self.__left = left

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, right):
        self.__right = right


class BinaryTree:
    def __init__(self):
        # 멤버는 루트 노드를 가리키는 root 하나입니다
        self.root = None

    # 루트 노드 반환
    def get_root(self):
        return self.root

    # 루트 노드 설정
    def set_root(self, r):
        self.root = r

    # 새로운 노드를 만들어 반환
    def make_node(self):
        new_node = TreeNode()
        return new_node

    # 노드의 데이터 반환
    def get_node_data(self, cur):
        return cur.get_data()

    # 노드의 데이터 설정
    def set_node_data(self, cur, data):
        cur.set_data(data)

    # 왼쪽 서브 트리 반환
    def get_left_sub_tree(self, cur):
        return cur.left

    # 오른쪽 서브 트리 반환
    def get_right_sub_tree(self, cur):
        return cur.right

    # 왼쪽 서브 트리를 만듭니다
    def make_left_sub_tree(self, cur, left):
        cur.left = left

    # 오른쪽 서브 트리를 만듭니다
    def make_right_sub_tree(self, cur, right):
        cur.right = right


if __name__ == "__main__":
    # 이진트리 객체 생성
    bt = BinaryTree()
    # 노드 생성
    # 이진 트리 객체로 노드를 생성
    n1 = bt.make_node()
    bt.set_node_data(n1, 1)
    # 노드 데이터 설정
    # 마찬가지로 이진 트리 객체로 노드의 데이터를 설정
    n2 = bt.make_node()
    bt.set_node_data(n2, 2)

    n3 = bt.make_node()
    bt.set_node_data(n3, 3)

    n4 = bt.make_node()
    bt.set_node_data(n4, 4)

    n5 = bt.make_node()
    bt.set_node_data(n5, 5)

    n6 = bt.make_node()
    bt.set_node_data(n6, 6)

    n7 = bt.make_node()
    bt.set_node_data(n7, 7)