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
        self.arrival_round_counter = 0 
        self.used_rooms = set()
 
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

    @timer
    def add_and_reaccommodate(self, new_guests_list):
        self.all_guests_ever.extend(new_guests_list)
        print(f"\nRe-accommodating for ALL {len(self.all_guests_ever)} guests...")

        used_rooms = set()
        self.room_map = HashTable()
        self.__root = None

        sorted_guests = sorted(self.all_guests_ever, key=lambda g: g.preferred_room)

        for guest in sorted_guests:
            final_room = guest.preferred_room
            while final_room in used_rooms:
                final_room += 1
            
            guest.room = final_room
            used_rooms.add(final_room)
            self.room_map.insert(guest.room, guest)
            self.__root = self.__tree.insert(self.__root, guest)

        self.all_guests_ever = sorted_guests
        
        self.arrival_round_counter += 1
        print("Full re-accommodation complete.")

    @timer
    def sortbytheway(self):
        
        print("\nSorting by actual room number (AVL Tree order)...")
        self.listsort = self.__tree.inOrder(self.__root)

        print(f"Sort completed. {len(self.listsort)} guests sorted.\n")

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
    def get_total_guests(self):
        return len(self.room_map)
    
    @timer
    def add_rooms_manual(self, room_number, list_channel):
        aircraft_id = list_channel[0]
        barge_id = list_channel[1]
        car_id = list_channel[2]
        new_guest_temp = Guest(0, aircraft_id, barge_id, car_id, room_number)

        preferred_room, final_room = self.room_map.insert2(room_number, new_guest_temp) 

        if preferred_room != final_room:
            print(f"\n--- Room Collision Detected! ---")
            print(f"Room {preferred_room} is occupied. The next available room is {final_room}.")
        
            decision = input(f"Do you want to: (1) Take room {final_room}, (2) Choose another room, or (3) Cancel addition? (1/2/3): ")
            
            if decision == "1":
            
                final_room_to_use = final_room
                
            elif decision == "2":
                
                try:
                    new_manual_room = int(input("Enter new room number: "))
                    print(f"Attempting to add guest to room {new_manual_room}...")
                    self.add_rooms_manual(new_manual_room, list_channel)
                    return 
                except ValueError:
                    print("Invalid input. Cancelling addition.")
                    return
                    
            elif decision == "3":
                print("Room addition cancelled.")
                return

            else:
                print("Invalid choice. Taking the next available room by default.")
                final_room_to_use = final_room
                
        else:
            final_room_to_use = final_room
            
        new_guest_final = Guest(0, aircraft_id, barge_id, car_id, final_room_to_use)

        if preferred_room != final_room_to_use:
            self.room_map._internal_insert2(final_room_to_use, new_guest_final)

        self.__root = self.__tree.insert(self.__root, new_guest_final)

        print(f"Guest successfully added to room {final_room_to_use}.")

        self.all_guests_ever.append(new_guest_final)

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