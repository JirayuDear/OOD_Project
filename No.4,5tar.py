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
    

class Hotel:
    def __init__(self):
        self.__root = None
        self.__tree = AVLTree()
        self.channel_map = {}
        self.room_map = {}
        self.last_barge_id = 0
        self.listsort = []
 
    @property
    def get_tree(self):
        return self.__tree
    
    @property
    def get_root(self):
        return self.__root
 
    def add_guests_info(self, list_channel):
        for item in list_channel:
            barge_id = item["barge"]
            self.last_barge_id = barge_id + 1  

            for cars_id, count in item["cars"].items():
                channel = f"barge{barge_id}_car{cars_id}"  
                guest_list = []

                for guest_num in range(count):
                    room_number = (2**guest_num) * (3**cars_id) * (5**barge_id)
                    new_guest = Guest(channel, guest_num, room_number)
                    self.__root = self.__tree.insert(self.__root, new_guest)

                    self.room_map[room_number] = new_guest
                    guest_list.append(new_guest)


                # if channel not in self.channel_map:
                #     self.channel_map[channel] = []

                #     # เพิ่มข้อมูลโครงสร้าง barge+cars
                #     self.channel_map[channel].append({
                #         "barge": barge_id,
                #         "cars": {cars_id: count}
                #     })

                # self.channel_map[channel].extend(guest_list)

                # print(f"Added {count} guests from channel {channel}.\n")


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

    def sort(self):
        self.listsort = self.__tree.inOrder(self.__root)
        

    def show_all_guests(self): ##อันนี้แสดงแขกทั้งหมด สร้างไว้ test code ว่าทำงานถูกมั้ย##
        #listsort = self.__tree.inOrder(self.__root)
        #print(self.__tree.printTree(self.__root))
        for guest in self.listsort:
            print(guest)

    def search_room(self, room_number):
        guest = self.room_map.get(room_number, None)
        if guest:
            print(f"Found Guest: {guest}")
            return guest
        else:
            print(f"Room {room_number} not found.")
            return None

    def get_total_guests(self): ##อันนี้คืนค่าจำนวนแขกทั้งหมด##
        return len(self.room_map)

    def add_rooms_manual_custom(self, channel, room_numbers):
        added_guests = []
        for order, room_number in enumerate(room_numbers):

            if room_number in self.room_map:
                print(f"Room {room_number} already occupied!")
                print(f"Please choose other room TT")
                return None
            new_guest = Guest(channel, order, room_number)
            self.__root = self.__tree.insert(self.__root, new_guest)
            self.room_map[room_number] = new_guest
            added_guests.append(new_guest)

        if added_guests:
            print(f"Added {len(added_guests)} guests manually to channel '{channel}'")
        return added_guests
    
    def add_rooms_manual(self, channel, count):
        added_guests = []
        room = self.__tree.inOrder(self.__root)
        last_room = room[-1]
        last_room = last_room.room
        for order in range(count):
            room_number = last_room + order
            if room_number in self.room_map:
                print(f"Room {room_number} already occupied! Skipping...")
                continue
            new_guest = Guest(channel, order, room_number)
            self.__root = self.__tree.insert(self.__root, new_guest)
            self.room_map[room_number] = new_guest
            added_guests.append(new_guest)

        if added_guests:
            print(f"Added {len(added_guests)} guests manually to channel '{channel}'")
        return added_guests
    
    def delete_room_manual(self, room_number):
        if room_number not in self.room_map:
            print(f"Room {room_number} not found! can't delete")
            return None
        
        guest = self.room_map[room_number]
        self.__root = self.__tree.delete(self.__root, room_number)
        del self.room_map[room_number]
        print(f"Deleted Guest {guest}")
        return guest

def menu():
    hotel = Hotel()
    avl = AVLTree()

    while True:
        print("\n====== Hilbert's Hotel Menu ======")
        print("1. Add Guests")
        print("2. Add Room Manual")
        print("3. Delete Room Manual")
        print("4. Sort Rooms")
        print("5. Search Room")
        print("6. Show All Guests")
        print("00. Exit")
        print("===================================\n")

        choice = input("Choose an option: ")

        if choice == "1":
            try:
                num_barges = int(input("Enter number of barges: "))
                num_cars = int(input("Enter number of cars per barge: "))
                num_people = int(input("Enter number of people per car: "))
            except ValueError:
                print("Invalid number, try again.")
                num_barges = num_cars = num_people = 0

            start_barge_id = hotel.last_barge_id if hotel.last_barge_id > 0 else 0

            list_channel = [
                {"barge": start_barge_id + b, "cars": {c: num_people for c in range(num_cars)}}
                for b in range(num_barges)
            ]

            hotel.add_guests_info(list_channel)

        elif choice == "2":
            try:
                channel = input("Enter channel name: ")
                mode = input("Choose mode: (c) เอาห้องเรียงกันมั้ย or (l) เลือกห้องตามใจชอบ: ").lower()
                
                if mode == "c":
                    count = int(input("Enter number of guests: "))
                    hotel.add_rooms_manual(channel, count)
                
                elif mode == "l":
                    rooms_str = input("Enter room numbers separated by commas: ")
                    room_numbers = [int(x.strip()) for x in rooms_str.split(",")]
                    hotel.add_rooms_manual_custom(channel, room_numbers)

                else:
                    print("Invalid mode!")

            except ValueError:
                print("Invalid input, try again.")

        elif choice == "3":
            try:
                room_number = input("Choose room number to delete ")
                hotel.delete_room_manual(room_number)
            except ValueError:
                print("Invalid input, try again.")

        elif choice == "4":
            print("\n===Already Sorted Rooms ===")
            hotel.sort()
            

        elif choice == "5":
            try:
                room_number = int(input("Enter room number to search: "))
                hotel.search_room(room_number)
            except ValueError:
                print("Invalid room number!")

        elif choice == "6": ##เอาไว้โชว์ผลก่อน เทสๆ##
            # avl.printTree(hotel.get_root)
            hotel.show_all_guests()
            print("Total guests:", hotel.get_total_guests())

        elif choice == "00": 
            print("Exiting program...")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    menu()

## สำหรับคนที่ทำข้อ 2 อะ ถ้าอยากแก้ไขพวกจัดห้องมึงไปแก้ใน Hotel ได้นะ พวก method หรือเพิ่ม method ได้เลย ถ้าผิดก็เดะแก้ให้