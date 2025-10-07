from hotel import Hotel

def menu():
    hotel = Hotel()

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