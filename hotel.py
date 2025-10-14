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
        self.channel_map = {}         # เพิ่มบรรทัดนี้
        self.next_channel_id = 1      # เพิ่มบรรทัดนี้
 
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
    
    def cal_room(self, channel_name, channel_order):
        if channel_name not in self.channel_map:
            # ใช้จำนวนเฉพาะเพื่อลดโอกาสการชนกันของผลคูณ
            primes = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149]
            self.channel_map[channel_name] = primes[(self.next_channel_id -1) % len(primes)] * self.next_channel_id
            self.next_channel_id += 1
        
        channel_base_id = self.channel_map[channel_name]
        return channel_base_id * 1000 + (channel_order + 1)
    
    def display_guest_summary(self, message):
        print(f"\n--- {message} ---")
        if not self.all_guests_ever:
            print("The hotel is currently empty.")
            return
        
        print(f"Total guests: {len(self.all_guests_ever)}")
        
        # NEW: เพิ่มส่วนหัวตาราง
        print(f"\n  {'Channel':<25} | {'Order':<7} | Room")
        print(f"  {'-'*25} | {'-'*7} | {'-'*15}")

        display_list = self.all_guests_ever
        if len(display_list) > 6:
            for guest in display_list[:3]:
                print(guest)
            print("  ...")
            for guest in display_list[-3:]:
                print(guest)
        else:
            for guest in display_list:
                print(guest)
        print(f"  {'-'*25} | {'-'*7} | {'-'*15}\n")

    @timer
    def add_new_guests(self, arrival_data):
        print(f"\nAdding new guests and starting re-accommodation...")

        self.display_guest_summary("State BEFORE new guests arrival")

        newly_arrived_guests = []
        for channel in arrival_data:  # แก้ตรงนี้
            channel_name = channel['name']
            count = channel['count']
            for i in range(count):
                guest = Guest(channel_name=channel_name, channel_order=i)
                newly_arrived_guests.append(guest)
        
        self.add_guests_info(newly_arrived_guests)

        self.display_guest_summary("State AFTER new guests arrival")
        self.show_memory_usage()

    def add_guests_info(self, new_guests_list, is_initial=False):
        self.all_guests_ever.extend(new_guests_list)

        print(f"Calculating new rooms for all {len(self.all_guests_ever)} guests...")
        guests_with_new_rooms = []
        used_rooms = set()

        for guest in self.all_guests_ever:
            preferred_room = self.cal_room(guest.channel_name, guest.channel_order)
            final_room = preferred_room
            # จัดการการชนกันของหมายเลขห้อง (เผื่อสูตรคำนวณชนกัน)
            while final_room in used_rooms:
                final_room += 1
            
            guest.room = final_room
            used_rooms.add(final_room)
            guests_with_new_rooms.append(guest)
            
        # Rebuild data structures
        self.__root = None
        self.room_map = HashTable(size=int(len(self.all_guests_ever) / 0.7) + 16)

        for guest in guests_with_new_rooms:
            self.room_map.insert(guest.room, guest)
            self.__root = self.__tree.insert(self.__root, guest)
            
        self.listsort = []

    @timer
    def add_initial_guest(self, num_initial_guests):
        initial_guests = []
        for i in range(num_initial_guests):
            guest = Guest(channel_name="Initial Guest", channel_order=i)
            initial_guests.append(guest)
        self.add_guests_info(initial_guests)
        print("\nInitial guests have been accommodated.")
        self.display_guest_summary("Initial State of the Hotel")
        self.show_memory_usage()

    @timer
    def sortbytheway(self):
        
        print("\nSorting by actual room number (AVL Tree order)...")
        self.listsort = self.__tree.inOrder(self.__root)

        print(f"Sort completed. {len(self.listsort)} guests sorted.\n")
        self.show_memory_usage()

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

        self.show_memory_usage()

    @timer
    def search_room(self, room_number):
        guest = self.room_map.search(room_number)
        if guest is None:
            print("No member in this room.")
        else:
            print(guest)

        self.show_memory_usage()

    @timer
    def get_total_guests(self):
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
