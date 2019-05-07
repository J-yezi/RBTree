class RBNode:
    def __init__(self, val, color="R"):
        self.val = val
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def is_black_node(self):
        return self.color == "B"

    def is_red_node(self):
        return self.color == "R"

    def set_black_node(self):
        self.color = "B"

    def set_red_node(self):
        self.color = "R"

    def print(self):
        if self.left:
            self.left.print()
        print(self.val)
        if self.right:
            print(self.right)
        pass

'''
红黑树 五大特征
性质一：节点是红色或者是黑色；
性质二：根节点是黑色；
性质三：每个叶节点（NIL或空节点）是黑色；
性质四：每个红色节点的两个子节点都是黑色的（也就是说不存在两个连续的红色节点）；
性质五：从任一节点到其没个叶节点的所有路径都包含相同数目的黑色节点
'''

class RBTree:
    def __init__(self):
        self.root = None
        self.index = 1
        self.action = ""
        pass

    '''
     * 左旋示意图：对节点x进行左旋
     *     parent               parent
     *    /                       /
     *   node                   right
     *  / \                     / \
     * ln  right   ----->     node  ry
     *    / \                 / \
     *   ly ry               ln ly
     * 左旋做了三件事：
     * 1. 将right的左子节点ly赋给node的右子节点,并将node赋给right左子节点ly的父节点(ly非空时)
     * 2. 将right的左子节点设为node，将node的父节点设为right
     * 3. 将node的父节点parent(非空时)赋给right的父节点，同时更新parent的子节点为right(左或右)
    '''
    '''
    :param node: 要左旋的节点
    :return:
    '''
    def left_rotate(self, node):
        parent = node.parent
        right = node.right

        # 把右子子点的左子点节赋给右节点
        node.right = right.left
        if node.right:
            node.right.parent = node

        # 把node变成基右子节点的左子节点
        right.left = node
        node.parent = right

        # 右子节点的你节点更并行为原来节点的父节点
        right.parent = parent
        if not parent:
            self.root = right
        else:
            if parent.left == node:
                parent.left = right
            else:
                parent.right = right
        pass

    '''
     * 左旋示意图：对节点y进行右旋
     *        parent           parent
     *       /                   /
     *      node                left
     *     /    \               / \
     *    left  ry   ----->   ln  node
     *   / \                     / \
     * ln  rn                   rn ry
     * 右旋做了三件事：
     * 1. 将left的右子节点rn赋给node的左子节点,并将node赋给rn右子节点的父节点(left右子节点非空时)
     * 2. 将left的右子节点设为node，将node的父节点设为left
     * 3. 将node的父节点parent(非空时)赋给left的父节点，同时更新parent的子节点为left(左或右)
    '''
    '''
    :param node: 要右旋的节点
    :return:
    '''
    def right_rotate(self, node):
        parent = node.parent
        left = node.left

        node.left = left.right
        if node.left:
            node.left.parent = node

        left.right = node
        node.parent = left

        left.parent = parent
        if not parent:
            self.root = left
        else:
            if parent.left == node:
                parent.left = left
            else:
                parent.right = left
        pass

    def insert_node(self, node):
        if not self.root:
            self.root = node
            return

        cur = self.root
        while cur:
            if cur.val < node.val:
                if not cur.right:
                    node.parent = cur
                    cur.right = node
                    break
                cur = cur.right
                continue

            if cur.val > node.val:
                if not cur.left:
                    node.parent = cur
                    cur.left = node
                    break
                cur = cur.left
        pass

    '''
    插入node后，需要检查是否破坏了红黑树的特性，需要进行自行调整
    '''
    def check_node(self, node):
        # 情况一，情况二
        if self.root == node or self.root == node.parent:
            self.root.set_black_node()
            print("set black", node.val)
            return

        # parent是黑色，直接添加就行了
        if node.parent.is_black_node():
            return

        grand = node.parent.parent
        if not grand:
            self.check_node(node.parent)
            return

        # 情况三，还需要进行自检查，因为调整后grand节点变成红色了
        if grand.left and grand.left.is_red_node() and grand.right and grand.right.is_red_node():
            grand.left.set_black_node()
            grand.right.set_black_node()
            grand.set_red_node()
            self.check_node(grand)

        parent = node.parent
        # 情况四
        if parent.left == node and grand.right == node.parent:
            self.right_rotate(node.parent)
            self.check_node(parent)
            return
        if parent.right == node and grand.left == node.parent:
            self.left_rotate(node.parent)
            self.check_node(parent)
            return

        # 情况五，这里就不需要在进行自检查了，因为调整后grand节点还是黑色
        parent.set_black_node()
        grand.set_red_node()
        if parent.left == node and grand.left == node.parent:
            self.right_rotate(grand)
        if parent.right == node and grand.right == node.parent:
            self.left_rotate(grand)
        pass

    '''
    情况一：插入的新节点 N 是红黑树的根节点，这种情况下，我们把节点 N 的颜色由红色变为黑色，性质2（根是黑色）被满足。
        同时 N 被染成黑色后，红黑树所有路径上的黑色节点数量增加一个，性质5（从任一节点到其每个叶子的所有简单路径都
        包含相同数目的黑色节点）仍然被满足
    情况二：N 的父节点是黑色，这种情况下，性质4（每个红色节点必须有两个黑色的子节点）和性质5没有受到影响，不需要调整
    情况三：N 的父节点是红色（节点 P 为红色，其父节点必然为黑色），叔叔节点 U 也是红色。由于 P 和 N 均为红色，
        所有性质4被打破，此时需要进行调整。这种情况下，先将 P 和 U 的颜色染成黑色，再将 G 的颜色染成红色。
        此时经过 G 的路径上的黑色节点数量不变，性质5仍然满足。但需要注意的是 G 被染成红色后，
        可能会和它的父节点形成连续的红色节点，此时需要递归向上调整
    情况四：N 的父节点为红色，叔叔节点为黑色。节点 N 是 P 的右孩子，且节点 P 是 G 的左孩子。
        此时先对节点 P 进行左旋，调整 N 与 P 的位置。接下来按照情况五进行处理，以恢复性质4
    情况五：N 的父节点为红色，叔叔节点为黑色。N 是 P 的左孩子，且节点 P 是 G 的左孩子。
        此时对 G 进行右旋，调整 P 和 G 的位置，并互换颜色。经过这样的调整后，性质4被恢复，同时也未破坏性质5
    '''
    def add_node(self, node):
        self.action = "insert node {}".format(node.val)
        # 新添加的node都是红色节点
        self.insert_node(node)
        self.check_node(node)
        pass

    '''
    通过递归找出前驱或者后继节点，最后得到的是一个没有前驱和后继的节点，并且把路过的值都替换了
    得到的node的值就是我们要删除node的值
    '''
    def pre_delete_node(self, node):
        post_node = self.get_post_node(node)
        if post_node:
            node.val, post_node.val = post_node.val, node.val
            return self.pre_delete_node(post_node)
        pre_node = self.get_pre_node(node)
        if pre_node:
            pre_node.val, node.val = node.val, pre_node.val
            return self.pre_delete_node(pre_node)
        return node

    def delete_node(self, val):
        node = self.get_node(val)
        if not node:
            print("node error {}".format(val))
            return

        node = self.pre_delete_node(node)
        self.check_delete_node(node)
        self.real_delete_node(node)
        pass

    def real_delete_node(self, node):
        if self.root == node:
            self.root = None
            return
        if node.parent.left == node:
            node.parent.left = None
        if node.parent.right == node:
            node.parent.right = None
        return

    # 这里递归的使用是因为先处理当前node，处理后走该node的parent会比其他路径少一个黑色节点，然后有递归传入node.parent，继续处理parent
    def check_delete_node(self, node):
        # node是根节点或者node是红色节点，直接删除
        if self.root == node or node.is_red_node():
            return

        node_is_left = node.parent.left == node
        brother = node.parent.right if node_is_left else node.parent.left
        # node为红色，上面已经判断了，所以这里node为黑色，那么brother肯定不为空，parent肯定是黑色
        if brother.is_red_node():
            if node_is_left:
                self.left_rotate(node.parent)
            else:
                self.right_rotate(node.parent)
            node.parent.set_red_node()
            brother.set_black_node()
            self.check_delete_node(node)
            return

        # 上面旋转后再调整当前结构brother和parent的颜色
        all_none = not brother.left and not brother.right
        all_black = brother.left and brother.right and brother.left.is_black_node() and brother.right.is_black_node()
        if all_none or all_black:
            brother.set_red_node()
            if node.parent.is_red_node():
                # parent为红色，brother为黑色，并且没有子节点，调整parent和brother的颜色就行了
                node.parent.set_black_node()
                return
            # parent为黑色，需要递归进行处理，把parent的兄弟节点变成红色
            self.check_delete_node(node.parent)
            return

        brother_same_right_red = node_is_left and brother.right and brother.right.is_red_node()
        brother_same_left_red = not node_is_left and brother.left and brother.left.is_red_node()
        if brother_same_right_red or brother_same_left_red:
            # 旋转前，让brother设置成parent的颜色
            if node.parent.is_red_node():
                brother.set_red_node()
            else:
                brother.set_black_node()
            node.parent.set_black_node()

            if brother_same_right_red:
                brother.right.set_black_node()
                self.left_rotate(node.parent)
            else:
                brother.left.set_black_node()
                self.right_rotate(node.parent)
            return

        # 兄弟节点的异侧子节点存在并且为红色
        brother_diff_right_red = not node_is_left and brother.right and brother.right.is_red_node()
        brother_diff_left_red = node_is_left and brother.left and brother.left.is_red_node()
        if brother_diff_right_red or brother_diff_left_red:
            brother.set_red_node()
            if brother_diff_right_red:
                brother.right.set_black_node()
                self.left_rotate(brother)
            else:
                brother.left.set_black_node()
                self.right_rotate(brother)

            self.check_delete_node(node)
            return

    '''
    获取前驱节点，node左子树的最大值
    '''
    def get_pre_node(self, node):
        if not node.left:
            return None
        pre_node = node.left
        while pre_node.right:
            pre_node = pre_node.right
        return pre_node

    '''
    获取后继节点，node右子树的最小值
    '''
    def get_post_node(self, node):
        if not node.right:
            return None
        post_node = node.right
        while post_node.left:
            post_node = post_node.left
        return post_node

    '''
    根据值查询节点信息
    '''
    def get_node(self, val):
        if not self.root:
            return None

        node = self.root
        while node:
            if node.val == val:
                break
            if node.val > val:
                node = node.left
                continue
            else:
                node = node.right
        return node