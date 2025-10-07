import time
from guest import Guest
from avl_tree import AVLTree
from HashTable import HashTable

class Hotel:
    def __init__(self):
        self.__root = None
        self.__tree = AVLTree()
        self.room_map = HashTable()
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
    
    def cal_room(self, guest_num, cars_id, barge_id, aircraft_id):
        room_number = (((guest_num+1)**2) * ((cars_id+1)**3) * ((barge_id+1)**5) * ((aircraft_id+1)**7))
        return room_number
    
    @timer
    def add_guests_info(self, arrival_data): 
        for aircraft in arrival_data:
            aircraft_id = aircraft["aircraft_id"]
            for barge in aircraft["barges"]:
                barge_id = barge["barge_id"]
                cars_iterable = [(car["car_id"], car["num_people"]) for car in barge["cars"]]
                for cars_id, count in cars_iterable:
                    channel = f"aircraft{aircraft_id}_barge{barge_id}_car{cars_id}"
                    for guest_num in range(count):
                        preferred_room = self.cal_room(guest_num, cars_id, barge_id, aircraft_id)

                        new_guest = Guest(channel, guest_num, preferred_room)
                        final_room_number = self.room_map.insert(preferred_room, new_guest)                      
                        new_guest.room = final_room_number
                        
                        self.__root = self.__tree.insert(self.__root, new_guest)

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
    def remove_guest_by_room(self, room_number):
        guest_to_remove = self.room_map.search(room_number)

        if guest_to_remove is None:
            print(f"Error: Room {room_number} not found or is empty. Cannot remove.")
            return None

        print(f"Found guest to remove: {guest_to_remove}")
        was_removed_from_map = self.room_map.remove(room_number)
        if not was_removed_from_map:
            print(f"Error: Failed to remove guest from room map. Data might be inconsistent.")
            return None
        
        print(f"Successfully removed from room map.")

        self.__root = self.__tree.delete(self.__root, room_number)
        print(f"Successfully removed from AVL tree.")
    
        self.listsort = []
        
        print(f"Successfully removed guest from room {room_number}.")
        return guest_to_remove
