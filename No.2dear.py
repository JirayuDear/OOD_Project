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

    def inOrder(self, root): ##เรียงแขกตามหมายเลขห้อง##
        if not root:
            return []
        
        return self.inOrder(root.left) + [root.guest] + self.inOrder(root.right)

class Hotel:
    def __init__(self):
        self.__root = None
        self.__tree = AVLTree()
        self.channel_map = {}
        self.room_map = {}

    def add_guests_info(self, list_channel):
        guest_list = []
        if len(list_channel) >=1:
            for item in list_channel:
                channel = item[0]
                count = item[1]
                for guest_num in range(count):
                    room_number = (2**guest_num)*(3**int(channel[-1]))
                    new_guest = Guest(channel, j, room_number)
                    self.__root = self.__tree.insert(self.__root, new_guest)

            # เก็บ hash
                    self.room_map[room_number] = new_guest
                    guest_list.append(new_guest)

                if channel not in self.channel_map:
                    self.channel_map[channel] = []
                self.channel_map[channel].extend(guest_list)

                print(f"Added {count} guests from channel {channel}.\n")

    def _is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

    def generate_prime_number(self, start_num: int) -> int:
        candidate = start_num + 1
        while True:
            if self._is_prime(candidate):
                return candidate
            candidate += 1

    def show_all_guests(self): ##อันนี้แสดงแขกทั้งหมด สร้างไว้ test code ว่าทำงานถูกมั้ย##
        guests = self.__tree.inOrder(self.__root)
        for guest in guests:
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
    
            for i in range(count_channels): ##วนรับช่องทางเข้ามาหลายช่องทาง พร้อมกัน##
                list_channel = []
                channel = input("Enter channel name: ").lower()
                channel = channel+'_'+str(i)
                count = int(input(f"Enter number of guests from channel {channel}: "))
                list_channel.append([channel, count])

            for item in list_channel:
                hotel.add_guests_info(list_channel)

        elif choice == "2":
            pass

        elif choice == "3":
            pass

        elif choice == "4":
            pass

        elif choice == "5":
            pass

        elif choice == "6":
            pass

        elif choice == "0": ##เอาไว้โชว์ผลก่อน เทสๆ##
            hotel.show_all_guests()
            print("Total guests:", hotel.get_total_guests())

        elif choice == "00": ##เอาไว้โชว์ผลก่อน เทสๆ##
            print("Exiting program...")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    menu()

## สำหรับคนที่ทำข้อ 2 อะ ถ้าอยากแก้ไขพวกจัดห้องมึงไปแก้ใน Hotel ได้นะ พวก method หรือเพิ่ม method ได้เลย ถ้าผิดก็เดะแก้ให้