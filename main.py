from hotel import Hotel

def menu():
    hotel = Hotel()
    try:
        initial_guest = int(input("Enter number of initial guests: "))
        hotel.add_initial_guest(initial_guest)
    except ValueError:
        print("Invalid number. Starting with 0 initial guests.")
        hotel.add_initial_guest(0)

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
            try:
                num_channels = int(input("Enter number of new arrival channels: "))
                arrival_channels = []
                for i in range(num_channels):
                    name = input(f"Enter name for channel #{i+1}: ")
                    count = int(input(f"Enter number of guests from channel '{name}': "))
                    if count < 0: raise ValueError
                    arrival_channels.append({'name': name, 'count': count})
                
                if arrival_channels:
                    hotel.add_new_guests(arrival_channels)

            except ValueError:
                print("Invalid input. Please enter valid names and positive numbers.")
                continue
            
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
