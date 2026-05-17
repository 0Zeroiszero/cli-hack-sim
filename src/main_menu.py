def menu():
    while True:
        print("==== HACKER NETWORK SYSTEM ====")
        print("1. Login")
        print("2. Tambah Server")
        print("3. Tampilkan Server")
        print("4. Hubungkan Server")
        print("5. Cari Jalur")
        print("6. Kirim Paket")
        print("7. Log Aktivitas")
        print("0. Keluar")

        choice = input("Please select an option: ")

        if choice == '1':
            print("Logging in...")
            # Add code to handle login here
            return
        elif choice == '2':
            print("Adding server...")
            # Add code to handle adding a server here
            return
        elif choice == '3':
            print("Tampilkan server...")
            # Add code to handle displaying servers here
            return
        elif choice == '4':
            print("Hubungkan ke server...")
            # Add code to handle connecting to a server here
            return
        elif choice == '5':
            print("Cari jalur...")
            # Add code to handle searching for routes here
            return
        elif choice == '6':
            print("Kirim paket...")
            # Add code to handle sending packets here
            return
        elif choice == '7':
            print("Menampilkan log aktivitas...")
            # Add code to handle displaying activity logs here
            return
        elif choice == '0':
            print("Keluar...")
            break
        else:
            print("Invalid option, please try again.")
            return

if __name__ == "__main__":
    menu()