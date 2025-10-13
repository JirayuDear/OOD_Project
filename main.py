from hotel import Hotel

def menu():
    hotel = Hotel()
    initial_guest = int(input("Enter number of initial guest: "))
    hotel.add_initial_guest(initial_guest)

    while True:
        print("\n====== Hilbert's Hotel Menu ======")
        print("1. Add Guests")
        print("2. Add Room Manual")
        print("3. Delete Room Manual")
        print("4. Sort Rooms")
        print("5. Search Room")
        print("6. Show All Guests")
        print("7. Export Guest Data to File")  # << เพิ่มบรรทัดนี้

        print("00. Exit")
        print("===================================\n")


        choice = input("Choose an option: ")

        if choice == "1":
            try:
                num_aircrafts = int(input("Enter number of aircrafts in this new group: "))
                num_barges = int(input("Enter number of barges per aircraft: "))
                num_cars = int(input("Enter number of cars per barge: "))
                num_people = int(input("Enter number of people per car: "))
            except ValueError:
                print("Invalid number, try again.")
                continue
                
            arrival_data = []
            start_aircraft_id = hotel.last_aircraft_id
            for i in range(num_aircrafts):
                ac_id = start_aircraft_id + i
                aircraft_info = {"aircraft_id": ac_id,"barges": []}
                for b_id in range(num_barges):
                    barge_info = {"barge_id": b_id,"cars": []}
                    for c_id in range(num_cars): 
                        car_info = {"car_id": c_id,"num_people": num_people}
                        barge_info["cars"].append(car_info)
                        
                    aircraft_info["barges"].append(barge_info)
                
                arrival_data.append(aircraft_info)
            hotel.add_new_guests(arrival_data)

        elif choice == "2":
            try:
                aircraft_id = int(input("Enter ID of aircrafts : "))
                barge_id = int(input("Enter ID of barges: "))
                car_id = int(input("Enter ID of cars per barge: "))

                room_number = int(input("Enter room number: "))
                
                list_id = [aircraft_id, barge_id, car_id]
                hotel.add_rooms_manual(room_number, list_id)
            except ValueError:
                print("Invalid input, try again.")

        elif choice == "3":
            try:
                room_number = int(input("Choose room number to delete "))
                hotel.remove_guest_by_room(room_number)
            except ValueError:
                print("Invalid input, try again.")

        elif choice == "4":
            hotel.sortbytheway()
            print("\n===Already Sorted Rooms ===")
            

        elif choice == "5":
            try:
                room_number = int(input("Enter room number to search: "))
                hotel.search_room(room_number)
            except ValueError:
                print("Invalid room number!")

        elif choice == "6": ##เอาไว้โชว์ผลก่อน เทสๆ##
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
