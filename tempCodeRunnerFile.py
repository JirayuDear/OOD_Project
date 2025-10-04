class Guest: ##เก็บข้อมูลช่องทางเข้ามา ลำดับแขก(เอาไว้ดูกรณีมาหลายคนเฉยๆ) แล้วก็เลขห้องนะ##
    def __init__(self, channel, order, room):
        self.channel = channel
        self.order = order
        self.room = room

    def __repr__(self):
        return f"Guest(channel={self.channel}, order={self.order}, room={self.room})"

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

    def inOrder(self, root,listkeep=None): ##เรียงแขกตามหมายเลขห้อง##
        if listkeep is None:
            listkeep = []

        if not root:
            return listkeep
        
        self.inOrder(root.left,listkeep)
        listkeep.append(root.guest)
        self.inOrder(root.right,listkeep)
        
        return listkeep

class Hotel:
    def __init__(self):
        self.__root = None
        self.__tree = AVLTree()
        self.channel_map = {}
        self.room_map = {}

    def add_guests_channel(self, channel, count): 
        guest_list = []
        for j in range(count):
            room_number = self.get_total_guests()
            new_guest = Guest(channel, j, room_number)

            self.__root = self.__tree.insert(self.__root, new_guest)

            # เก็บใน hash เพื่อ lookup O(1)
            self.room_map[room_number] = new_guest
            guest_list.append(new_guest)
            self.temp_room = j
        # อัปเดต channel map
        if channel not in self.channel_map:
            self.channel_map[channel] = []
        self.channel_map[channel].extend(guest_list)

        print(f"Added {count} guests from channel {channel}.\n")
    
    def show_all_guests(self): 
        listsort = self.__tree.inOrder(self.__root)
        for guest in listsort:
            print(guest)

    def get_total_guests(self): ##อันนี้คืนค่าจำนวนแขกทั้งหมด##
        return len(self.room_map)
    
def menu():
    hotel = Hotel()

    while True:
        print("\n====== Hilbert's Hotel Menu ======")
        print("1. Add Guests (ฟังก์ชัน 1)")
        print("2. Add More Guests (ฟังก์ชัน 2)")
        print("3. Add Room Manual (ฟังก์ชัน 3)")
        print("4. Delete Room Manual (ฟังก์ชัน 4)")
        print("5. Sort Rooms (ฟังก์ชัน 5)")
        print("6. Search Room (ฟังก์ชัน 6)")
        print("0. Exit") 
        print("===================================\n")

        choice = input("Choose an option: ")

        if choice == "1":
            try:
                count_channels = int(input("Enter number of channels: "))
            except ValueError:
                print("Invalid number, try again.")
                continue
            
            for _ in range(count_channels): ##วนรับช่องทางเข้ามาหลายช่องทาง##
                channel = input("Enter channel name: ").lower()
                count = int(input(f"Enter number of guests from channel {channel}: "))
                hotel.add_guests_channel(channel, count)

        elif choice == "2":
            pass

        elif choice == "3":
            pass

        elif choice == "4":
            pass

        elif choice == "5":
            print("\n=== Sorted Rooms ===")
            hotel.show_all_guests()

        elif choice == "6":
            pass

        elif choice == "0": ##เอาไว้โชว์ผลก่อน เทสๆ##
            print("Total guests:", hotel.get_total_guests())
            print("Exiting program...")

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    menu()

## สำหรับคนที่ทำข้อ 2 อะ ถ้าอยากแก้ไขพวกจัดห้องมึงไปแก้ใน Hotel ได้นะ พวก method หรือเพิ่ม method ได้เลย ถ้าผิดก็เดะแก้ให้