import time
from guest import Guest
from avl_tree import AVLTree

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
    
    def timer(func):
        def wrapper(*args, **kwargs): 
            start = time.perf_counter()
            result = func(*args, **kwargs) 
        
            end = time.perf_counter()
            print(f"\n'{func.__name__}' runtime: {end - start:.6f} sec") 
            return result
        return wrapper
    
    def cal_room(self, guest_num, cars_id, barge_id):
        room_number = ((guest_num+1)**2) * ((cars_id+1)**3) * ((barge_id+1)**5)
        return room_number
 
    @timer
    def add_guests_info(self, list_channel):
        for item in list_channel:
            barge_id = item["barge"]
            self.last_barge_id = barge_id + 1  

            for cars_id, count in item["cars"].items():
                channel = f"barge{barge_id}_car{cars_id}"  
                guest_list = []

                for guest_num in range(count):
                    room_number = ((guest_num+1)**2) * ((cars_id+1)**3) * ((barge_id+1)**5)
                    new_guest = Guest(channel, guest_num, room_number)
                    self.__root = self.__tree.insert(self.__root, new_guest)

                    self.room_map[room_number] = new_guest
                    guest_list.append(new_guest)
    @timer
    def sort(self):
        self.listsort = self.__tree.inOrder(self.__root)
        
    @timer
    def show_all_guests(self): ##อันนี้แสดงแขกทั้งหมด สร้างไว้ test code ว่าทำงานถูกมั้ย##
        # listsort = self.__tree.inOrder(self.__root)
        # print(self.__tree.printTree(self.__root))
        for guest in self.listsort:
            print(guest)

    @timer
    def search_room(self, room_number):
        guest = self.room_map.get(room_number, None)
        if guest:
            print(f"Found Guest: {guest}")
            return guest
        else:
            print(f"Room {room_number} not found.")
            return None

    @timer
    def get_total_guests(self): ##อันนี้คืนค่าจำนวนแขกทั้งหมด##
        return len(self.room_map)
    
    @timer
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
    
    @timer
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
    
    @timer
    def delete_room_manual(self, room_number):
        if room_number not in self.room_map:
            print(f"Room {room_number} not found! can't delete")
            return None
        
        guest = self.room_map[room_number]
        self.__root = self.__tree.delete(self.__root, room_number)
        del self.room_map[room_number]
        print(f"Deleted Guest {guest}")
        return guest