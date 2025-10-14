from guest import Guest

class AVLNode:
    def __init__(self, guest):
        self.guest = guest
        self.left = None
        self.right = None
        self.height = 1

class AVLTree: ##อันนี้แชทแนะนำมาเอาไว้มันบอกช่วยให้เพิ่ม ค้นหาห้องได้เร็ว##
    def __getHight(self, node):
        return node.height if node else 0
    
    def __getBalance(self, node):
        return self.__getHight(node.left) - self.__getHight(node.right) if node else 0

    def __rotateRight(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2

        y.height = 1 + max(self.__getHight(y.left), self.__getHight(y.right))
        x.height = 1 + max(self.__getHight(x.left), self.__getHight(x.right))

        return x
    
    def __rotateLeft(self, y):
        x = y.right
        T3 = x.left
        x.left = y
        y.right = T3

        y.height = 1 + max(self.__getHight(y.left), self.__getHight(y.right))
        x.height = 1 + max(self.__getHight(x.left), self.__getHight(x.right))

        return x
    
    def insert(self, root, guest): ##แทรกแขกใหม่ด้วยการใช้หมายเลขห้อง##
        if not root:
            return AVLNode(guest)
        elif guest.room < root.guest.room:
            root.left = self.insert(root.left, guest)
        else:
            root.right = self.insert(root.right, guest)

        root.height = 1 + max(self.__getHight(root.left), self.__getHight(root.right))
        balance = self.__getBalance(root)

        if balance > 1 and guest.room < root.left.guest.room:
            return self.__rotateRight(root)
        
        if balance < -1 and guest.room > root.right.guest.room:
            return self.__rotateLeft(root)
        
        if balance > 1 and guest.room > root.left.guest.room:
            root.left = self.__rotateLeft(root.left)
            return self.__rotateRight(root)
        
        if balance < -1 and guest.room < root.right.guest.room:
            root.right = self.__rotateRight(root.right)
            return self.__rotateLeft(root)

        return root

    def insert2(self, root, guest): ##แทรกแขกใหม่ด้วยการใช้หมายเลขห้อง##
        if not root:
            return AVLNode(guest)
        elif guest.room < root.guest.room:
            root.left = self.insert(root.left, guest)
        else:
            root.right = self.insert(root.right, guest)

        root.height = 1 + max(self.__getHight(root.left), self.__getHight(root.right))
        balance = self.__getBalance(root)

        if balance > 1 and guest.room < root.left.guest.room:
            return self.__rotateRight(root)
        
        if balance < -1 and guest.room > root.right.guest.room:
            return self.__rotateLeft(root)
        
        if balance > 1 and guest.room > root.left.guest.room:
            root.left = self.__rotateLeft(root.left)
            return self.__rotateRight(root)
        
        if balance < -1 and guest.room < root.right.guest.room:
            root.right = self.__rotateRight(root.right)
            return self.__rotateLeft(root)

        return root
    
    def inOrder(self, root,listkeep=None): ##เรียงแขกตามหมายเลขห้อง##
        if listkeep is None:
            listkeep = []

        if not root:
            return listkeep
        
        self.inOrder(root.left,listkeep)
        listkeep.append(root.guest)
        self.inOrder(root.right,listkeep)
        
        return listkeep
    
    def __getMinValueNode(self, node):
        current = node
        while current.left:
            current = current.left
        return current
    def delete(self, root, room_number):
        if not root:
            return root
        

        if room_number < root.guest.room:
            root.left = self.delete(root.left, room_number)
        elif room_number > root.guest.room:
            root.right = self.delete(root.right, room_number)
        else:

            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            

            temp = self.__getMinValueNode(root.right)
            root.guest = temp.guest
            root.right = self.delete(root.right, temp.guest.room)
        

        root.height = 1 + max(self.__getHight(root.left), self.__getHight(root.right))

        balance = self.__getBalance(root)

    
        if balance > 1 and self.__getBalance(root.left) >= 0:
            return self.__rotateRight(root)
        if balance > 1 and self.__getBalance(root.left) < 0:
            root.left = self.__rotateLeft(root.left)
            return self.__rotateRight(root)

        if balance < -1 and self.__getBalance(root.right) <= 0:
            return self.__rotateLeft(root)
        if balance < -1 and self.__getBalance(root.right) > 0:
            root.right = self.__rotateRight(root.right)
            return self.__rotateLeft(root)

        return root

    def printTree(self, node, level=0):
        if node is not None:
            self.printTree(node.right, level + 1)
            print('     ' * level, node.guest)
            self.printTree(node.left, level + 1)

    def writeInOrder(self, node, f):
        if node:
            self.writeInOrder(node.left, f)
            guest = node.guest
            f.write(f"{guest.get_channel_string()}\torder{guest.order}\t{guest.room}\n")
            self.writeInOrder(node.right, f)
