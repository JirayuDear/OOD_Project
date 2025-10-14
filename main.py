from hotel import Hotel
from guest import Guest
import math

prime_cache = {}
def generate_primes(count):
    if count in prime_cache:
        return prime_cache[count]
    primes = []
    num = 2
    while len(primes) < count:
        is_p = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_p = False
                break
        if is_p:
            primes.append(num)
        num += 1
        prime_cache[count] = primes # เก็บผลลัพธ์ลง cache
    return primes

def calculate_room_dynamically(guest_order, channel_ids, primes):
    room_number = (guest_order + 1) ** primes[0]
    for i, channel_id in enumerate(channel_ids):
        prime_exponent = primes[i + 1]
        room_number *= ((channel_id + 1) ** prime_exponent)
    return room_number

def create_guests_recursive(data, channel_names, primes, current_ids, guest_list, arrival_round): # CHANGED
    if not data: return
    if "num_people" in data[0]:
        for item in data:
            item_id = item["id"]
            num_people = item["num_people"]
            final_ids = current_ids + [item_id]
            for i in range(num_people):
                pref_room = calculate_room_dynamically(i, final_ids, primes)
                guest = Guest(order=i, channel_ids=final_ids, preferred_room=pref_room, 
                              channel_names=channel_names, arrival_round=arrival_round)
                guest_list.append(guest)
        return

    for item in data:
        item_id = item["id"]
        new_ids = current_ids + [item_id]
        create_guests_recursive(item.get("sub_channels", []), channel_names, primes, new_ids, guest_list, arrival_round)

def prompt_for_arrivals_recursive(channel_names, parent_name=None):

    if not channel_names:
        try:
            prompt = f"  -> Enter number of 'people' per '{parent_name}': "
            num_people = int(input(prompt))
            return {"num_people": num_people}
        except (ValueError, TypeError): 
            print("   -> Invalid value, defaulting to 1 person.")
            return {"num_people": 1}

    current_channel_name = channel_names[0]
    remaining_channels = channel_names[1:]
    
    try:
        if parent_name:
            prompt = f"-> Enter number of '{current_channel_name}s' per '{parent_name}': "
        else:
            prompt = f"-> Enter total number of '{current_channel_name}s': "
        
        count = int(input(prompt))
    except ValueError: 
        print(f" -> Invalid value, defaulting to 1 {current_channel_name}.")
        count = 1
 
    items = []
    for i in range(count):
        print(f"--- (Configuring '{current_channel_name}' ID {i}) ---")
        sub_data = prompt_for_arrivals_recursive(remaining_channels, parent_name=current_channel_name)
        
        if "num_people" in sub_data:
            items.append({"id": i, "num_people": sub_data["num_people"]})
        else:
            items.append({"id": i, "sub_channels": sub_data})
            
    return items

def menu():
    hotel = Hotel()
    try:
        initial_guest_count = int(input("Enter number of initial guests: "))
        if initial_guest_count > 0:
            initial_channels = ["initial"]
            initial_primes = generate_primes(2) 
            initial_guests_list = []
            
            current_round = hotel.arrival_round_counter

            for i in range(initial_guest_count):
                pref_room = calculate_room_dynamically(guest_order=0, channel_ids=[i], primes=initial_primes)
                
                guest = Guest(order=0, 
                              channel_ids=[i], 
                              preferred_room=pref_room, 
                              channel_names=initial_channels,
                              arrival_round=current_round)
                
                initial_guests_list.append(guest)
            hotel.add_and_reaccommodate(initial_guests_list)

    except ValueError:
        print("must be Integer")

    sortbytheway = False

    while True:
        print("\n====== Hilbert's Hotel Menu ======")
        print("1. Add Guests")
        print("2. Add Room Manual")
        print("3. Delete Room Manual")
        print("4. Sort Rooms")
        print("5. Search Room")
        print("6. Show All Guests")
        print("7. Export Guest Data to File") 

        print("00. Exit")
        print("===================================\n")


        choice = input("Choose an option: ")

        if choice == "1":
            channel_input = input("\nEnter channel(Ex. ship,car): ")
            channel_names = [name.strip() for name in channel_input.split(',')]
            
            if not channel_names:
                print("Error one channel at least")
                continue

            primes = generate_primes(len(channel_names) + 1)
            current_round = hotel.arrival_round_counter
            arrival_data = prompt_for_arrivals_recursive(channel_names)

            newly_arrived_guests = []
            create_guests_recursive(arrival_data, channel_names, primes, [], newly_arrived_guests, current_round)
            
            hotel.add_and_reaccommodate(newly_arrived_guests)

        elif choice == "2":
            channel_input = input("\nEnter channel(Ex. ship,car): ")
            channel_names = [name.strip() for name in channel_input.split(',')]
            
            if not channel_names:
                print("Error one channel at least")
                continue

            primes = generate_primes(len(channel_names) + 1)
            current_round = hotel.arrival_round_counter
            arrival_data = prompt_for_arrivals_recursive(channel_names)

            manual_guests = []
            create_guests_recursive(arrival_data, channel_names, primes, [], manual_guests, current_round)
            
            hotel.add_rooms_manual(manual_guests)

        elif choice == "3":
            try:
                room_number = int(input("Choose room number to delete "))
                hotel.remove_guest_by_room(room_number)
                if sortbytheway == True:
                    hotel.sortbytheway()
            except ValueError:
                print("Invalid input, try again.")

        elif choice == "4":
            hotel.sortbytheway()
            sortbytheway = True
            print("\n===Already Sorted Rooms ===")
            

        elif choice == "5":
            try:
                room_number = int(input("Enter room number to search: "))
                hotel.search_room(room_number)
            except ValueError:
                print("Invalid room number!")

        elif choice == "6":
            hotel.show_all_guests()
            print("Total guests:", hotel.get_total_guests())

        elif choice == "7":
            hotel.export_guest_data()

        elif choice == "00": 
            print("Exiting program...")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    menu()
