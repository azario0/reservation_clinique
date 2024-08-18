import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime
import csv
import os
from datetime import datetime

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DoctorOfficeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Doctor's Office Reservation System")
        self.geometry("800x600")

        self.csv_file = "reservations.csv"
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Surname", "Phone", "Date", "Time"])

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_new = self.tabview.add("New Reservation")
        self.tab_today = self.tabview.add("Today's Reservations")
        self.tab_manage = self.tabview.add("Manage Reservations")

        self.setup_new_reservation_tab()
        self.setup_today_reservations_tab()
        self.setup_manage_reservations_tab()

        self.csv_file = "reservations.csv"
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Surname", "Phone", "Date", "Time"])

    def setup_new_reservation_tab(self):
        frame = ctk.CTkFrame(self.tab_new)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = ctk.CTkEntry(frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Surname:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.surname_entry = ctk.CTkEntry(frame)
        self.surname_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.phone_entry = ctk.CTkEntry(frame)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Date:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Time:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.time_entry = ctk.CTkEntry(frame)
        self.time_entry.grid(row=4, column=1, padx=5, pady=5)

        submit_button = ctk.CTkButton(frame, text="Submit", command=self.submit_reservation)
        submit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=20)

    def setup_today_reservations_tab(self):
        self.today_frame = ctk.CTkScrollableFrame(self.tab_today)
        self.today_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.update_today_reservations()

    def setup_manage_reservations_tab(self):
        frame = ctk.CTkFrame(self.tab_manage)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(frame, text="Rechercher par:").grid(row=0, column=0, padx=5, pady=5)
        self.search_option = ctk.CTkOptionMenu(frame, values=["Nom", "Date"], command=self.toggle_search_input)
        self.search_option.grid(row=0, column=1, padx=5, pady=5)

        self.search_entry = ctk.CTkEntry(frame)
        self.search_entry.grid(row=0, column=2, padx=5, pady=5)

        self.date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=0, column=2, padx=5, pady=5)
        self.date_entry.grid_remove()  # Cacher initialement le widget de date

        search_button = ctk.CTkButton(frame, text="Rechercher", command=self.search_reservations)
        search_button.grid(row=0, column=3, padx=5, pady=5)

        self.results_frame = ctk.CTkScrollableFrame(frame)
        self.results_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def toggle_search_input(self, choice):
        if choice == "Nom":
            self.search_entry.grid()
            self.date_entry.grid_remove()
        else:
            self.search_entry.grid_remove()
            self.date_entry.grid()

    def submit_reservation(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        phone = self.phone_entry.get()
        date = self.date_entry.get_date().strftime("%Y-%m-%d")
        time = self.time_entry.get()

        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, surname, phone, date, time])

        self.name_entry.delete(0, 'end')
        self.surname_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.time_entry.delete(0, 'end')

        self.update_today_reservations()

    def update_today_reservations(self):
        
        for widget in self.today_frame.winfo_children():
            widget.destroy()

        today = datetime.now().strftime("%Y-%m-%d")
        with open(self.csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 5:  # Ensure the row has at least 5 elements
                    if row[3] == today:
                        frame = ctk.CTkFrame(self.today_frame)
                        frame.pack(fill="x", padx=5, pady=5)
                        ctk.CTkLabel(frame, text=f"{row[0]} {row[1]}").pack(side="left", padx=5)
                        ctk.CTkLabel(frame, text=f"Time: {row[4]}").pack(side="right", padx=5)
                else:
                    print(f"Skipping invalid row: {row}")

    def search_reservations(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        search_type = self.search_option.get()
        if search_type == "Nom":
            search_value = self.search_entry.get().lower()
        else:
            search_value = self.date_entry.get_date().strftime("%Y-%m-%d")

        with open(self.csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Ignorer l'en-tête
            for row in reader:
                if len(row) >= 5:  # S'assurer que la ligne a au moins 5 éléments
                    if (search_type == "Nom" and search_value in f"{row[0]} {row[1]}".lower()) or \
                       (search_type == "Date" and search_value == row[3]):
                        frame = ctk.CTkFrame(self.results_frame)
                        frame.pack(fill="x", padx=5, pady=5)
                        ctk.CTkLabel(frame, text=f"{row[0]} {row[1]} - {row[3]} {row[4]}").pack(side="left", padx=5)
                        ctk.CTkButton(frame, text="Modifier", command=lambda r=row: self.modify_reservation(r)).pack(side="right", padx=5)
                        ctk.CTkButton(frame, text="Supprimer", command=lambda r=row: self.delete_reservation(r)).pack(side="right", padx=5)
                else:
                    print(f"Ligne invalide ignorée : {row}")

    def modify_reservation(self, reservation):
        modify_window = ctk.CTkToplevel(self)
        modify_window.title("Modify Reservation")
        modify_window.geometry("300x600")

        ctk.CTkLabel(modify_window, text="Name:").pack(padx=5, pady=5)
        name_entry = ctk.CTkEntry(modify_window)
        name_entry.insert(0, reservation[0])
        name_entry.pack(padx=5, pady=5)

        ctk.CTkLabel(modify_window, text="Surname:").pack(padx=5, pady=5)
        surname_entry = ctk.CTkEntry(modify_window)
        surname_entry.insert(0, reservation[1])
        surname_entry.pack(padx=5, pady=5)

        ctk.CTkLabel(modify_window, text="Phone:").pack(padx=5, pady=5)
        phone_entry = ctk.CTkEntry(modify_window)
        phone_entry.insert(0, reservation[2])
        phone_entry.pack(padx=5, pady=5)

        ctk.CTkLabel(modify_window, text="Date:").pack(padx=5, pady=5)
        date_entry = DateEntry(modify_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        # Convert the date string to a datetime object
        date_obj = datetime.strptime(reservation[3], "%Y-%m-%d").date()
        date_entry.set_date(date_obj)
        date_entry.pack(padx=5, pady=5)

        ctk.CTkLabel(modify_window, text="Time:").pack(padx=5, pady=5)
        time_entry = ctk.CTkEntry(modify_window)
        time_entry.insert(0, reservation[4])
        time_entry.pack(padx=5, pady=5)

        def save_changes():
            new_reservation = [name_entry.get(), surname_entry.get(), phone_entry.get(),
                            date_entry.get_date().strftime("%Y-%m-%d"), time_entry.get()]
            self.update_reservation(reservation, new_reservation)
            modify_window.destroy()
            self.search_reservations()
            self.update_today_reservations()  # Update today's reservations after modifying

        ctk.CTkButton(modify_window, text="Save Changes", command=save_changes).pack(padx=5, pady=20)

    def update_reservation(self, old_reservation, new_reservation):
        rows = []
        with open(self.csv_file, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        for i, row in enumerate(rows):
            if row == old_reservation:
                rows[i] = new_reservation
                break

        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def delete_reservation(self, reservation):
        rows = []
        with open(self.csv_file, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        rows = [row for row in rows if row != reservation]

        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        self.search_reservations()
        self.update_today_reservations()
        
if __name__ == "__main__":
    app = DoctorOfficeApp()
    app.mainloop()