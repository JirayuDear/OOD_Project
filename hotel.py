import time
from guest import Guest
from avl_tree import AVLTree
from HashTable import HashTable
import sys

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
        self.show_memory_usage()

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
        self.show_memory_usage()


    @timer
    def sortbytheway(self):
        print("\n=== Sort Options ===")
        print("1. Sort by arrival channel (aircraft → barge → car IDs)")
        print("2. Sort by arrival order number")
        print("3. Sort by actual room number (default AVL order)")
        choice = input("Choose sort type: ").strip()

        
        guests = [item[1] for item in self.room_map.table if item and item != self.room_map._DELETED]

        if not guests:
            print("No guests to sort.")
            return

        if choice == "1":
            
            print("\nSorting by (aircraft_id, barge_id, car_id)...")
            self.listsort = sorted(guests, key=lambda g: (g.aircraft_id, g.barge_id, g.car_id))

        elif choice == "2":
           
            print("\nSorting by order number...")
            self.listsort = sorted(guests, key=lambda g: g.order)

        elif choice == "3":
            
            print("\nSorting by actual room number (AVL Tree order)...")
            self.listsort = self.__tree.inOrder(self.__root)

        else:
            print("Invalid choice. Sorting by actual room number (default).")
            self.listsort = self.__tree.inOrder(self.__root)

        print(f"✅ Sort completed. {len(self.listsort)} guests sorted.\n")

        

    @timer
    def show_all_guests(self):
        import sys
        if not self.listsort:
            for slot in self.room_map.table:
                if slot is not None and slot != self.room_map._DELETED:
                    guest = slot[1]
                    print(guest, flush=True)
        else:
            for guest in self.listsort:
                print(guest, flush=True)


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
        final_room = self.room_map.insert(room_number, new_guest)
        new_guest = Guest(0, aircraft_id, barge_id, car_id, final_room)
        self.__root = self.__tree.insert(self.__root, new_guest)

        if room_number != final_room:
            print(f"The room number cannot be issued.")
            print(f"Your room is {final_room}")

        self.all_guests_ever.append(new_guest)
        self.show_memory_usage()

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
        self.show_memory_usage()
        return guest_to_remove
    
    @timer
    def export_guest_data(self, filename="guest_result.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Channel\tOrder\tRoom\n")
            f.write("=============================\n")
            self.__tree.writeInOrder(self.__root, f)

    
    @staticmethod
    def get_deep_size(obj, seen=None):
        """คำนวณหน่วยความจำทั้งหมดของ obj รวมของที่อ้างอิงอยู่ภายใน"""
        size = sys.getsizeof(obj)
        if seen is None:
            seen = set()
        obj_id = id(obj)
        if obj_id in seen:
            return 0
        seen.add(obj_id)

        if isinstance(obj, dict):
            size += sum(Hotel.get_deep_size(k, seen) + Hotel.get_deep_size(v, seen) for k, v in obj.items())
        elif hasattr(obj, '__dict__'):
            size += Hotel.get_deep_size(vars(obj), seen)
        elif isinstance(obj, (list, tuple, set, frozenset)):
            size += sum(Hotel.get_deep_size(i, seen) for i in obj)
        return size

    def show_memory_usage(self):
        """ฟังก์ชันแสดงหน่วยความจำหลังแต่ละการทำงาน"""
        print("\n=== Memory Usage Report ===")
        print(f"HashTable: {self.get_deep_size(self.room_map):,} bytes")
        print(f"AVL Tree: {self.get_deep_size(self.__tree):,} bytes")
        print(f"All Guest Records: {self.get_deep_size(self.all_guests_ever):,} bytes")
        total = (
            self.get_deep_size(self.room_map)
            + self.get_deep_size(self.__tree)
            + self.get_deep_size(self.all_guests_ever)
        )
        print(f"Total Memory Usage: {total:,} bytes")
        print("============================\n")
