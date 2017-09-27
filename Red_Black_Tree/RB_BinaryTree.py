import random
import sys


class Node:
    __slots__ = ['mData', 'mColor', 'mLeft', 'mRight', 'mParent']

    RED = True
    BLACK = False

    def __init__(self, data, color=RED):
        if not type(color) == bool:
            raise TypeError("Bad value for color parameter, expected True/False but given %s" % color)
        self.mColor = color
        self.mData = data
        self.mLeft = self.mRight = self.mParent = NilNode()

    def __nonzero__(self):
        return True

    def __bool__(self):
        return True


class NilNode(Node):
    __instance__ = None

    def instance(self):
        if self.__instance__ is None:
            self.__instance__ = NilNode()
        return self.__instance__

    def __init__(self):
        self.mColor = Node.BLACK
        self.mData = None
        self.mLeft = self.mRight = self.mParent = None

    def __nonzero__(self):
        return False

    def __bool__(self):
        return False


class RBTree:
    __slots__ = ['mRoot', 'mSize', 'mCtr']

    def __init__(self):
        self.mRoot = NilNode()
        self.mSize = 0
        self.mCtr = 1

    def __str__(self):
        return ("(root.mSize = %d)\n" % self.mSize) + str(self.mRoot)

    def generate_str(self):

        intro = "digraph BST{\n\tnode [fontname=\"Helvetica\"];"
        middle = ""
        middle = self.traverseLeft(self.mRoot)
        end = "\n}"

        return intro + middle + end

    def traverseLeft(self, n):

        r = ""

        if n is None:
            r += "Tree is empty!\n"
        else:

            if n.mLeft.mData is None and n.mRight.mData is None:
                val1 = str(n.mData)
                i1 = str(self.mCtr)
                i2 = str(self.mCtr + 1)
                i2 = str(self.mCtr + 1)
                self.mCtr += 2

                r += val1 + " -> null" + i1 + ";\n\t"
                r += "\n\tnull" + i1 + " [shape=point color=\"black\"];\n\t"

                r += val1 + " -> null" + i2 + ";"
                r += "\n\tnull" + i2 + " [shape=point color=\"black\"];\n\t"


            elif n.mLeft.mData is None and n.mRight.mData is not None:
                val1 = str(n.mData)
                val2 = str(n.mRight.mData)
                i1 = str(self.mCtr)
                self.mCtr += 1

                r += "\n\tnull" + i1 + " [shape=point color=\"black\"];\n\t"
                r += val1 + " -> null" + i1 + ";"

                r += "\n\t" + val1 + " -> " + val2 + ";"
                r += "\n\t" + val2
                r += " [color=\"red\"];" if n.mRight.mColor == Node.RED else " [color=\"black\"];"

            elif n.mLeft.mData is not None and n.mRight.mData is None:
                val1 = str(n.mData)
                val2 = str(n.mLeft.mData)
                i1 = str(self.mCtr)
                self.mCtr += 1

                r += "\n\t" + val1 + " -> " + val2 + ";"
                r += "\n\t" + val2
                r += " [color=\"red\"];" if n.mLeft.mColor == Node.RED else " [color=\"black\"];"

                r += "\n\tnull" + i1 + " [shape=point color=\"black\"];\n\t"
                r += val1 + " -> null" + i1 + ";"

            else:
                val1 = str(n.mData)
                val2 = str(n.mLeft.mData)
                val3 = str(n.mRight.mData)

                r += "\n\t" + val1 + " -> " + val2 + ";"
                r += "\n\t" + val2
                r += " [color=\"red\"];" if n.mLeft.mColor == Node.RED else " [color=\"black\"];"

                r += "\n\t" + val1 + " -> " + val3 + ";"
                r += "\n\t" + val3
                r += " [color=\"red\"];" if n.mRight.mColor == Node.RED else " [color=\"black\"];"

            if n.mLeft.mData is not None:
                r = r + self.traverseLeft(n.mLeft)

            if n.mRight.mData is not None:
                r = r + self.traverseLeft(n.mRight)

            return r

    def insert(self, data):
        self.add(Node(data))

    def add(self, n):
        self.__insert_helper(n)

        n.mColor = Node.RED

        while n != self.mRoot and n.mParent.mColor == Node.RED:
            if n.mParent == n.mParent.mParent.mLeft:
                m = n.mParent.mParent.mRight
                if m and m.mColor == Node.RED:
                    n.mParent.mColor = Node.BLACK
                    m.mColor = Node.BLACK
                    n.mParent.mParent.mColor = Node.RED
                    n = n.mParent.mParent
                else:
                    if n == n.mParent.mRight:
                        n = n.mParent
                        self.__left_rotate(n)
                    n.mParent.mColor = Node.BLACK
                    n.mParent.mParent.mColor = Node.RED
                    self.__right_rotate(n.mParent.mParent)
            else:
                m = n.mParent.mParent.mLeft
                if m and m.mColor == Node.RED:
                    n.mParent.mColor = Node.BLACK
                    m.mColor = Node.BLACK
                    n.mParent.mParent.mColor = Node.RED
                    n = n.mParent.mParent
                else:
                    if n == n.mParent.mLeft:
                        n = n.mParent
                        self.__right_rotate(n)
                    n.mParent.mColor = Node.BLACK
                    n.mParent.mParent.mColor = Node.RED
                    self.__left_rotate(n.mParent.mParent)
        self.mRoot.mColor = Node.BLACK

    def remove(self, data):
        self.removeAt(data, self.mRoot)
        return True

    def removeAt(self, data, n):

        if n is None:
            return "Data does not exist!"

        if data < n.mData:
            self.removeAt(data, n.mLeft)
        elif data > n.mData:
            self.removeAt(data, n.mRight)
        else:
            return self.delete(n)

    def delete(self, n):
        if not n.mLeft or not n.mRight:
            y = n
        else:
            y = self.successor(n)
        if not y.mLeft:
            x = y.mRight
        else:
            x = y.mLeft
        x.mParent = y.mParent

        if not y.mParent:
            self.mRoot = x
        else:
            if y == y.mParent.mLeft:
                y.mParent.mLeft = x
            else:
                y.mParent.mRight = x

        if y != n:
            n.mData = y.mData

        if y.mColor == Node.BLACK:
            self.__delete_fixup(x)

        self.mSize -= 1
        self.mCtr -= 1
        return y

    def minimum(self, n=None):
        if n is None:
            n = self.mRoot

        while n.mLeft:
            n = n.mLeft

        return n

    def maximum(self, n=None):
        if n is None:
            n = self.mRoot

        while n.mRight:
            n = n.mRight

        return n

    def successor(self, n):
        if n.mRight:
            return self.minimum(n.mRight)

        m = n.mParent
        while m and n == m.mRight:
            n = m
            m = m.mParent

        return m

    def predecessor(self, n):
        if n.mLeft:
            return self.maximum(n.mLeft)

        m = n.mParent
        while m and n == m.mLeft:
            n = m
            m = m.mParent

        return m

    def inorder_walk(self, n=None):
        if n is None:
            n = self.mRoot

        n = self.minimum()
        while n:
            yield n.mData
            n = self.successor(n)

    def reverse_inorder_walk(self, n=None):
        if n is None:
            n = self.mRoot

        n = self.maximum()
        while n:
            yield n.mData
            n = self.predecessor(n)

    def search(self, data, n=None):
        if n is None:
            n = self.mRoot

        while n and n.mData != data:
            if data < n.mData:
                n = n.mLeft
            else:
                n = n.mRight

        return n

    def is_empty(self):
        return bool(self.mRoot)

    def black_height(self, n=None):
        if x is None:
            n = self.mRoot

        height = 0
        while n:
            n = n.mLeft
            if not n or n.is_black():
                height += 1

        return height

    def __left_rotate(self, n):
        if not n.mRight:
            raise "n.mRight is nil!"

        m = n.mRight
        n.mRight = m.mLeft
        if m.mLeft:
            m.mLeft.mParent = n

        m.mParent = n.mParent
        if not n.mParent:
            self.mRoot = m
        else:
            if n == n.mParent.mLeft:
                n.mParent.mLeft = m
            else:
                n.mParent.mRight = m

        m.mLeft = n
        n.mParent = m

    def __right_rotate(self, n):
        if not n.mLeft:
            raise "n.mLeft is nil!"

        m = n.mLeft
        n.mLeft = m.mRight
        if m.mRight:
            m.mRight.mParent = n

        m.mParent = n.mParent
        if not n.mParent:
            self.mRoot = m
        else:
            if n == n.mParent.mLeft:
                n.mParent.mLeft = m
            else:
                n.mParent.mRight = m

        m.mRight = n
        n.mParent = m

    def __insert_helper(self, n):
        y = NilNode()
        x = self.mRoot
        while x:
            y = x
            if n.mData < x.mData:
                x = x.mLeft
            else:
                x = x.mRight

        n.mParent = y
        if not y:
            self.mRoot = n
        else:
            if n.mData < y.mData:
                y.mLeft = n
            else:
                y.mRight = n

        self.mSize += 1

    def __delete_fixup(self, x):
        while x != self.mRoot and x.mColor == Node.BLACK:
            if x == x.mParent.mLeft:
                w = x.mParent.mRight
                if w.mColor == Node.RED:
                    w.mColor = Node.BLACK
                    x.mParent.mColor = Node.RED
                    self.__left_rotate(x.mParent)
                    w = x.mParent.mRight
                if w.mLeft.mColor == Node.BLACK and w.mRight.mColor == Node.BLACK:
                    w.mColor = Node.RED
                    x = x.mParent
                else:
                    if w.mRight.mColor == Node.BLACK:
                        w.mLeft.mColor = Node.BLACK
                        w.mColor = Node.RED
                        self.__right_rotate(w)
                        w = x.mParent.mRight
                    w.mColor = x.mParent.mColor
                    x.mParent.mColor = Node.BLACK
                    w.mRight.mColor = Node.BLACK
                    self.__left_rotate(x.mParent)
                    x = self.mRoot
            else:
                w = x.mParent.mLeft
                if w.mColor == Node.RED:
                    w.mColor = Node.BLACK
                    x.mParent.mColor = Node.RED
                    self.__right_rotate(x.mParent)
                    w = x.mParent.mLeft
                if w.mRight.mColor == Node.BLACK and w.mLeft.mColor == Node.BLACK:
                    w.mColor = Node.RED
                    x = x.mParent
                else:
                    if w.mLeft.mColor == Node.BLACK:
                        w.mRight.mColor = Node.BLACK
                        w.mColor = Node.RED
                        self.__left_rotate(w)
                        w = x.mParent.mLeft
                    w.mColor = x.mParent.mColor
                    x.mParent.mColor = Node.BLACK
                    w.mLeft.mColor = Node.BLACK
                    self.__right_rotate(x.mParent)
                    x = self.mRoot
        x.mColor = Node.BLACK


def writeRBTree(tree, file):
    dot_text = tree.generate_str()

    file.write(dot_text)
    file.write('\n')


def main():
    if len(sys.argv) < 2:
        print('Please provide the number of keys to enter.')
        sys.exit(1)

    numOfKeys = int(sys.argv[1])
    # parts = int(s/3)
    myTree = RBTree()
    insertRange = list(range(1,numOfKeys + 1))

    print('Randomly inserting the numbers from 1 to {}.'.format(len(insertRange)))

    random.shuffle(insertRange)

    for i in insertRange:
        myTree.insert(i)

    file_to = open('output.dot', 'w')
    writeRBTree(myTree, file_to)
    file_to.flush()
    file_to.close()
    print('\nTo compile, run: $ dot -Tpng output.dot -o output.png')

    """
    random.shuffle(r)

    for n in range(1, 3):
        m = r[(n-1) * parts : (n * parts)]
        print(len(m))

        for i in m:
            print('removed {}'.format(i))
            v = t.remove(i)
            if v:
                print('\tcompleted.')
            else:
                print('\terror.')
        c = chr(n + 97)
        filename = str(c) + '.dot'
        f = open(filename, 'w')
        writeRBTree(t, f)
        f.flush()
        f.close()
    """


if __name__ == '__main__':
    main()
