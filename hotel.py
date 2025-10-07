import time
from guest import Guest
from avl_tree import AVLTree
from HashTable import HashTable

class Hotel:
    def __init__(self):
        self.__root = None
        self.__tree = AVLTree()
        self.room_map = HashTable()
        self.last_aircraft_id = 0
        self.listsort = []
        self.all_guests_ever = []
 
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
    def add_new_guests(self, arrival_data):
        print(f"\nAdding new guests and starting re-accommodation...")
        newly_arrived_guests = []
        for aircraft in arrival_data:
            aircraft_id = aircraft["aircraft_id"]
            self.last_aircraft_id = max(self.last_aircraft_id, aircraft_id + 1)
            for barge in aircraft["barges"]:
                barge_id = barge["barge_id"]
                cars_iterable = [(car["car_id"], car["num_people"]) for car in barge["cars"]]
                for cars_id, count in cars_iterable:
                    for guest_num in range(count):
                        guest = Guest(order=guest_num, aircraft_id=aircraft_id, barge_id=barge_id, car_id=cars_id)
                        newly_arrived_guests.append(guest)
        self.add_guests_info(newly_arrived_guests)

    def add_guests_info(self, new_guests_list, is_initial=False):
        if is_initial:
            self.all_guests_ever = new_guests_list
        else:
            self.all_guests_ever.extend(new_guests_list)

        print(f"Calculating new rooms for all {len(self.all_guests_ever)} guests...")
        guests_with_new_rooms = []
        used_rooms = set()

        for guest in self.all_guests_ever:
            a_id, b_id, c_id = 0, 0, 0
            if guest.aircraft_id == -1:
                a_id, b_id, c_id = 0, 0, 0
            else:
                a_id, b_id, c_id = guest.aircraft_id, guest.barge_id, guest.car_id

            preferred_room = self.cal_room(guest.order, c_id, b_id, a_id)
            final_room = preferred_room
            while final_room in used_rooms:
                final_room += 1
            
            guest.room = final_room
            used_rooms.add(final_room)
            guests_with_new_rooms.append(guest)
            
        self.__root = None
        self.room_map = HashTable(size=int(len(self.all_guests_ever) / 0.7) + 16)

        for guest in guests_with_new_rooms:
            self.room_map.insert(guest.room, guest)
            self.__root = self.__tree.insert(self.__root, guest)
            
        self.listsort = []

    @timer
    def add_initial_guest(self, num_initial_guests):
        initial_guests_list = []
        
        for i in range(num_initial_guests):
            room_num = i + 1 
            guest = Guest(order=i, aircraft_id=-1, barge_id=-1, car_id=-1, room=room_num)
            self.room_map.insert(guest.room, guest)
            self.__root = self.__tree.insert(self.__root, guest)
            initial_guests_list.append(guest)
        self.all_guests_ever.extend(initial_guests_list)

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
        guest = self.room_map.search(room_number)
        if guest is None:
            print("No member in this room.")
        else:
            print(guest)


    @timer
    def get_total_guests(self): ##อันนี้คืนค่าจำนวนแขกทั้งหมด##
        return len(self.room_map)
    
    @timer
    def add_rooms_manual(self, room_number, list_channel):
        aircraft_id = list_channel[0]
        barge_id = list_channel[1]
        car_id = list_channel[2]

        new_guest = Guest(0, aircraft_id, barge_id, car_id, room_number)
        self.__root = self.__tree.insert(self.__root, new_guest)
        final_room = self.room_map.insert(room_number, new_guest)

        if room_number != final_room:
            print(f"The room number cannot be issued.")
            print(f"Your room is {final_room}")

        self.all_guests_ever.append(new_guest)


    
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
