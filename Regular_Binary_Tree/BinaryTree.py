# Created by Charles Bucher on 4/6/17.
# Copyright 2017 Charles Bucher. All rights reserved.

# All code was created by Charles Bucher.

import random
import sys
import string


class Node:
    __slots__ = ['mData', 'mRight', 'mLeft', 'mParent']

    def __init__(self, data=-1):
        self.mData = data
        self.mLeft = Node
        self.mLeft = None
        self.mRight = Node
        self.mRight = None
        self.mParent = Node
        self.mParent = None

    def setData(self, data):
        self.mData = data

    def setRight(self, right):
        self.mRight = right

    def setLeft(self, left):
        self.mLeft = left

    def setParent(self, parent):
        self.mParent = parent


class Tree:
    __slots__ = ['mRoot', 'mCount', 'nCtr', 'iterHelp']

    def __init__(self):
        self.mRoot = Node
        self.mRoot = None
        self.mCount = 0
        self.nCtr = 1
        self.iterHelp = self.mRoot

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

            if n.mLeft is None and n.mRight is None:
                val1 = str(n.mData)
                i1 = str(self.nCtr)
                i2 = str(self.nCtr + 1)
                self.nCtr += 2

                r += "\n\tnull" + i1 + " [shape=point];\n\t"
                r += val1 + " -> null" + i1 + ";\n\t"

                r += "null" + i2 + " [shape=point];\n\t"
                r += val1 + " -> null" + i2 + ";"


            elif n.mLeft is None and n.mRight is not None:
                val1 = str(n.mData)
                val2 = str(n.mRight.mData)
                i1 = str(self.nCtr)
                self.nCtr += 1

                r += "\n\tnull" + i1 + " [shape=point];\n\t"
                r += val1 + " -> null" + i1 + ";"

                r += "\n\t" + val1 + " -> " + val2 + ";"

            elif n.mLeft is not None and n.mRight is None:
                val1 = str(n.mData)
                val2 = str(n.mLeft.mData)
                i1 = str(self.nCtr)
                self.nCtr += 1

                r += "\n\t" + val1 + " -> " + val2 + ";\n\t"

                r += "null" + i1 + " [shape=point];\n\t"
                r += val1 + " -> null" + i1 + ";"

            else:
                val1 = str(n.mData)
                val2 = str(n.mLeft.mData)
                val3 = str(n.mRight.mData)

                r += "\n\t" + val1 + " -> " + val2 + ";"
                r += "\n\t" + val1 + " -> " + val3 + ";"

            if n.mLeft is not None:
                r = r + self.traverseLeft(n.mLeft)

        if n.mRight is not None:
            r = r + self.traverseLeft(n.mRight)

        return r

    def insert(self, data):

        if self.mRoot is None:
            newNode = Node(data)
            self.mRoot = newNode
            self.mCount += 1
        else:
            self.addAt(data, self.mRoot)

    def addAt(self, data, n):

        if data < n.mData:
            if n.mLeft is None:
                newNode = Node(data)
                n.setLeft(newNode)
                newNode.setParent(n)
                self.mCount += 1
            else:
                self.addAt(data, n.mLeft)

        elif data > n.mData:
            if n.mRight is None:
                newNode = Node(data)
                n.setRight(newNode)
                newNode.setParent(n)
                self.mCount += 1
            else:
                self.addAt(data, n.mRight)

    def findMaximum(self, n):

        if n.mRight is None:
            return n

        return self.findMaximum(n.mRight)

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
            return self.removeNode(n)

    def removeNode(self, n):

        if self.mRoot is None:
            return "Cannot remove from an empty tree!"

        if n.mLeft is None and n.mRight is None:
            if n is self.mRoot:
                self.mRoot = None
            elif n.mParent.mLeft is n:
                n.mParent.setLeft(None)
            elif n.mParent.mRight is n:
                n.mParent.setRight(None)

            self.mCount -= 1

        elif n.mLeft is None or n.mRight is None:
            if n is self.mRoot:
                if n.mLeft is not None:
                    self.mRoot = n.mLeft
                    n.setParent(None)
                else:
                    self.mRoot = n.mRight
                    n.setParent(None)

                self.mCount -= 1

            elif n.mParent.mLeft is n:
                if n.mLeft is not None:
                    n.mParent.setLeft(n.mLeft)
                    n.mLeft.setParent(n.mParent)
                else:
                    n.mParent.setLeft(n.mRight)
                    n.mRight.setParent(n.mParent)

                self.mCount -= 1

            elif n.mParent.mRight is n:
                if n.mLeft is not None:
                    n.mParent.setRight(n.mLeft)
                    n.mLeft.setParent(n.mParent)
                else:
                    n.mParent.setRight(n.mRight)
                    n.mRight.setParent(n.mParent)

                self.mCount -= 1
            else:
                l = self.findMaximum(n.mLeft)
                n.setData(l.mData)
                self.removeNode(l)

        return n


def writeTree(tree, file):
    dot_text = tree.generate_str()

    file.write(dot_text)
    file.write('\n')


def main():
    if len(sys.argv) < 2:
        print('Please provide the number of keys to enter.')
        sys.exit(1)
    s = int(sys.argv[1])
    parts = int(s / 3)
    t = Tree()
    r = list(range(1, s + 1))

    print('Randomly inserting the numbers from 1 to {}.'.format(len(r)))

    random.shuffle(r)

    for i in r:
        t.insert(i)

    f = open('a.dot', 'w')
    writeTree(t, f)
    f.flush()
    f.close()
    print('To compile, run: $ dot -Tpng a.dot -o a.png')

    # Code commented out outpus two other .dot files that show examples of
    # randomly removing sections of the tree.
    """
    random.shuffle(r)
    
    for n in range(1, 3):
        m = r[(n - 1) * parts: (n * parts)]
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
        writeTree(t, f)
        f.flush()
        f.close()
    """

if __name__ == "__main__":
    main()
