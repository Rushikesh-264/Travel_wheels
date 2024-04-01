from tkinter import *
import json
import os
from tkinter import messagebox
from tkinter import filedialog
from tkcalendar import Calendar
from PIL import ImageTk, Image
from datetime import datetime
from tkinter import StringVar
from tkinter.ttk import Combobox
import sqlite3

# Creating database tables
connect = sqlite3.connect("Car_Rental_Management_Database.db")
# Table for storing car information

connect.execute('''Create table if not exists Cars_info (Car_id INT (100,1) PRIMARY KEY, Car_number VARCHAR(9),
 Car_name VARCHAR(15), Seats_capacity VARCHAR(8), luggage_capacity VARCHAR(8), transmission_type VARCHAR (9),
  Fuel_type VARCHAR (6),car_type VARCHAR(8),  vehicle_rent VARCHAR(9))''')

# Table for storing Rented car details
connect.execute('''CREATE TABLE if not exists Rented_cars (Car_id INT(4), Car_no VARCHAR(9), Car_name VARCHAR(15),
    Customer_name VARCHAR(20), Customer_contact_number INT(10), Departure_date TIMESTAMP, Arrival_date TIMESTAMP)''')

# Table for storing rented car list
connect.execute('''Create table if not exists Rented_car_list (Car_id INT(4), Car_no VARCHAR(9), Car_name VARCHAR(15),
 Seats_capacity VARCHAR(8), luggage_capacity VARCHAR(8),transmission_type VARCHAR (9), Fuel_type VARCHAR (6),
 car_type VARCHAR(8), vehicle_rent VARCHAR(9))''')

# Table for storing Car history
connect.execute('''CREATE TABLE if not exists Car_history (Car_id INT(3), Car_name VARCHAR(15), Customer_name VARCHAR(25),
                 Departure_date TIMESTAMP, Arrival_date TIMESTAMP, Revenue_generated INT(8))''')

customer_frame = None
admin_frame = None
user = None
password_entry1 = None
car_history_details = []
button_pressed_before = False
total_fine = 0
departure_date = 0
removed_car = 0
new_car = 0
deleted_cars = {}
new_image_path = ''
new_car_name = ''
car_button = 0
car_names = []
car_data2_opened = 0
old_car_values = []
new_car_values = []
new_car_path_values = []


def create_divided_page():  # Creating the main window
    def close_window():
        window.destroy()

    # Create main window
    window = Tk()
    window.title("Divided Page")
    # Set window to full screen without taskbar
    window.attributes('-fullscreen', True)
    window.attributes('-topmost', True)

    # Calculate center position
    center_x = window.winfo_width() // 2

    # Create frames for the two sections
    frame1 = Frame(window, bg="black", width=center_x + 370, height=window.winfo_screenheight())
    frame1.pack(side="left", fill="both", expand=True)

    frame2 = Frame(window, bg="white", height=window.winfo_screenheight())
    frame2.pack(side="right", fill="both", expand=True)

    design_frame1 = Listbox(window, bg='#4287f5', width=157, height=50, highlightthickness=0, borderwidth=0)
    design_frame1.place(x=10, y=159)

    welcome_label = Label(frame1, text="Welcome to Travel Wheels", font=("Helvetica", 32, "bold"), fg="white",
                          bg="black")
    welcome_label.place(x='20', y='29')

    # Add label "Wherever you are headed, we've got the wheels to get you there" to the black section
    quote_label = Label(frame1,
                        text="                          Wherever you are headed, we've got the wheels to get you there",
                        font=("Helvetica", 16), fg="white", bg="black")
    quote_label.place(x='25', y='110')

    # Add some styling to the labels
    welcome_label.config(anchor="center")
    quote_label.config(anchor="center")

    heading_label = Label(frame2, text="ACCOUNT TYPE", font=("Helvetica", 26), bg="white")
    heading_label.place(relx=0.5, rely=0.1, anchor="center")

    customer_image = PhotoImage(file="images/customer.png")
    admin_image = PhotoImage(file="images/admin.png")

    side_image = Image.open('images/car_rent.png')
    photo = ImageTk.PhotoImage(side_image)
    side_image_label = Label(design_frame1, image=photo, bg='#4287f5', width=802, height=800)
    side_image_label.image = photo
    side_image_label.place(x=0, y=0)
    selected = StringVar()
    order_details = []

    def customer_clicked():  # to open the customer interface
        global customer_frame

        def toggle_calendar_visibility(event=None, entry=None):
            if not visibility_list[0]:
                if entry == "pick_up_date":
                    cal.place(in_=customer_frame, x=195, y=405)  # Adjust the coordinates for pick_up_date
                    cal.lift()  # Raise the calendar to the top
                    cal.bind("<<CalendarSelected>>", lambda event: get_selected_date(pick_up_date))
                elif entry == "drop_off_date":
                    cal.place(in_=customer_frame, x=550, y=405)  # Adjust the coordinates for drop_off_date
                    cal.lift()  # Raise the calendar to the top
                    cal.bind("<<CalendarSelected>>", lambda event: get_selected_date(drop_off_date))
                visibility_list[0] = True

        def get_selected_date(date_entry):
            selected_date_str = cal.get_date()
            selected_date = datetime.strptime(selected_date_str, "%m/%d/%y").date()
            current_date = datetime.now().date()

            # Check if the selected date is before the current date
            if selected_date < current_date:
                print("Please select a date from today onwards.")
                return

            formatted_date_str = selected_date.strftime("%d-%m-%Y")

            # Do something with the selected date, such as updating a label or variable
            print("Selected date:", formatted_date_str)
            order_details.append(formatted_date_str)

            # Insert the selected date into the textbox
            date_entry.delete(0, END)  # Clear the existing content
            date_entry.insert(0, selected_date_str)  # Insert the selected date

            # Hide the Calendar widget
            cal.place_forget()
            visibility_list[0] = False
            print("Calendar hidden")
            sub_heading.focus()

        def get_selected_date_drop_off(pick_up_date):
            selected_date_str = cal.get_date()
            selected_date = datetime.strptime(selected_date_str, "%m/%d/%y").date()
            current_date = datetime.now().date()

            # Check if the selected date is before the current date
            if selected_date < current_date:
                return

            # Check if the selected drop_off date is before the pick_up_date
            pick_up_date_str = pick_up_date.get()
            if not pick_up_date_str:
                return

            pick_up_date = datetime.strptime(pick_up_date_str, "%m/%d/%y").date()

            # Disable dates prior to the pick-up date in the drop-off date calendar
            cal.configure(date_pattern=['yyyy', '-mm-', '-dd'])
            cal.configure(minimum=pick_up_date)

            # Do something with the selected date, such as updating a label or variable
            print("Selected date:", selected_date)
            order_details.append(selected_date)

            # Insert the selected date into the textbox
            drop_off_date.delete(0, END)  # Clear the existing content
            drop_off_date.insert(0, selected_date_str)  # Insert the selected date

            # Hide the Calendar widget
            cal.place_forget()
            visibility_list[0] = False
            sub_heading.focus()

        if customer_frame is None:  # To display the main Customer Home Page Interface
            customer_frame = Frame(window, bg="black", width=900, height=900)
            customer_frame.place(x=0, y=0)

            heading = Label(customer_frame, text="Welcome to Travel Wheels", font=("Helvetica", 38, "bold"),
                            fg="yellow",
                            bg="#075a75", width=62, height=3, anchor="center", justify="center")
            heading.place(relx=0.5, rely=0.05, anchor="center")
            sub_heading = Label(customer_frame, text="Wherever you are headed, we've got the wheels to get you there",
                                font=("Helvetica", 20, "bold"), fg="yellow", bg="#075a75", width=50, height=1)
            sub_heading.place(x=325, y=88)

            mid_section = Listbox(customer_frame, fg="black", bg="blue", width=259, height=16, highlightthickness=2,
                                  borderwidth=2)
            mid_section.place(x=0, y=140)
            side_image = Image.open('images/jeep.png')
            photo = ImageTk.PhotoImage(side_image)

            side_image_label = Label(customer_frame, image=photo, bg='#1e85d0', height=269, width=1550)
            side_image_label.image = photo
            side_image_label.place(x=0, y=140)

            current_date = datetime.now()

            cal = Calendar(customer_frame, selectmode="day", year=current_date.year, month=current_date.month,
                           day=current_date.day)

            pick_up_label = Label(customer_frame, text="Pick-up Date", font=("Helvetica", 12), fg="black")
            pick_up_label.place(x=90, y=375)  # Adjust the coordinates as needed

            pick_up_date = Entry(customer_frame, bg="#e4eef0", width=15, highlightthickness=0, fg="black",
                                 font=("yu gothic ui semibold", 12))
            pick_up_date.place(x=200, y=375)  # Adjust the coordinates as needed

            pick_up_date.bind("<FocusIn>", lambda event: toggle_calendar_visibility(event, entry="pick_up_date"))
            pick_up_date.bind("<FocusOut>", lambda event: toggle_calendar_visibility(event, entry="pick_up_date"))
            pick_up_date.bind("<Button-1>", lambda event: toggle_calendar_visibility(event, entry="pick_up_date"))

            drop_off_label = Label(customer_frame, text="Drop-off Date", font=("Helvetica", 12), fg="black")
            drop_off_label.place(x=410, y=375)

            drop_off_date = Entry(customer_frame, bg="#e4eef0", width=15, highlightthickness=0, fg="black",
                                  font=("yu gothic ui semibold", 12))
            drop_off_date.place(x=530, y=375)  # Adjust the coordinates as needed

            drop_off_date.bind("<FocusIn>", lambda event: toggle_calendar_visibility(event, entry="drop_off_date"))
            drop_off_date.bind("<FocusOut>", lambda event: toggle_calendar_visibility(event, entry="drop_off_date"))
            drop_off_date.bind("<Button-1>", lambda event: toggle_calendar_visibility(event, entry="drop_off_date"))

            cal.bind("<<CalendarSelected>>",
                     lambda event: get_selected_date(pick_up_date if pick_up_date.focus_get() else drop_off_date))
            visibility_list = [False]

            pick_up_location_label = Label(customer_frame, text="Pick-up Location", font=("Helvetica", 12), fg="black")
            pick_up_location_label.place(x=750, y=375)

            pick_up_time_label = Label(customer_frame, text="Pick-up Time", font=("Helvetica", 12), fg="black")
            pick_up_time_label.place(x=1180, y=375)

            def select_time():
                time = time_var.get()
                print("Selected time:", time)
                order_details.append(time)

            def clear_time_selection():
                time_var.set("")  # Clear the time selection
                time_combobox.set("")  # Clear the combobox selection

            time_var = StringVar()
            time_combobox = Combobox(customer_frame, textvariable=time_var,
                                     values=["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM",
                                             "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM",
                                             "9:00 PM", "10:00 PM"])
            time_combobox.place(x=1300, y=375)

            def on_select(event):
                selected_location.set(location_combobox.get())
                order_details.append(selected_location.get())

            def clear_location_selection():
                selected_location.set("")  # Clear the selected location
                location_combobox.set("")  # Clear the combobox selection

            selected_location = StringVar()
            location_options = [  # Combobox for the pickup location options
                "Aakshwani",
                "Kranti Chowk",
                "Cidco N-6",
                "Cannaught Place",
                "Mahavir Chowk",
                "Cidco N- 5",
                "Chhatrapati Sambhajinagar Airport"
            ]
            selected_location = StringVar()

            # Create the ComboBox for the pick-up location option
            location_combobox = Combobox(customer_frame, values=location_options, textvariable=selected_location,
                                         state="readonly", font=("Helvetica", 12), width=24)
            location_combobox.bind("<<ComboboxSelected>>", on_select)
            location_combobox.place(x=880, y=375)  # Adjust the coordinates as needed

            def clear_and_show_main_window():
                order_details.clear()
                clear_location_selection()
                clear_time_selection()
                show_main_window("customer")

            back_button = Button(customer_frame, text="Back to Main", fg='Black', bg='#1b87d2',
                                 font=("yu gothic ui bold", 16), command=lambda: clear_and_show_main_window(),
                                 cursor='hand2')
            back_button.pack()
            back_button.place(x=1300, y=50)

            new_frame = Frame(customer_frame, width=1600, height=600, background='#daebf0')
            new_frame.place(x=0, y=410)

            text = Label(new_frame, text="ALL CARS", font=("Helvetica", 22, "bold"), fg="Black", bg='#daebf0',
                         anchor='center')
            text.place(x=680, y=3)

            def check_date_time():
                if not pick_up_date.get():
                    messagebox.showerror("Empty Fields", "Please select pick up date.")
                    return 0

                if not drop_off_date.get():
                    messagebox.showerror("Empty Fields", "Please select drop off date.")
                    return 0

                if not time_var.get():
                    messagebox.showerror("Empty Fields", "Please select pick up time.")
                    return 0

                if not selected_location.get():
                    messagebox.showerror("Empty Fields", "Please select pick up location.")
                    return 0
                else:
                    return 1

            # To display the terms and conditions
            def terms_and_conditions(booking_info_frame, customer_info_frame, car_info_frame):
                terms_and_conditions = [
                    "1. Rental Agreement:",

                    "The rental agreement is between TRAVEL WHEELS and the individual(s) listed as the renter(s) on "
                    "the rental agreement document.",

                    "2. Eligibility:",

                    "Renters must meet the minimum age requirement of 21 Years and hold a valid driver's license "
                    "issued by their country of residence.",

                    "3. Vehicle Use:",

                    "    The rented vehicle is to be used only by the authorized renter(s) and for lawful purposes.",
                    "    The vehicle shall not be used:",
                    "        For any illegal purposes.",
                    "        To transport goods or passengers for hire.",
                    "        To tow or push any vehicle or trailer.",
                    "    Smoking and the transportation of pets are strictly prohibited in the vehicle.",

                    "4. Rental Period:",

                    "    The rental period begins and ends at the dates and times specified in the rental agreement.",
                    "Any extension of the rental period must be agreed upon and confirmed by TRAVEL WHEELS in advance.",

                    "5. Payment and Fees:",

                    "    Rental charges are based on the rates agreed upon at the time of booking.",
                    "Additional charges may apply for late returns, fuel charges, tolls, parking fines and any "
                    "damages to the vehicle during the rental period.",
                    "Payment is due upon return of the vehicle and can be made by credit card or other approved "
                    "payment methods.",

                    "6. Insurance:",

                    "    The rented vehicle is covered by comprehensive insurance.",
                    "Renters are responsible for any deductibles or excess amounts in case of an accident or damage "
                    "to the vehicle.",

                    "7. Maintenance and Repairs:",

                    "Renters must promptly report any mechanical issues or damage to the vehicle to TRAVEL   WHEELS.",
                    "Repairs or maintenance to the vehicle must only be carried out with the approval of TRAVEL "
                    "WHEELS.",

                    "8. Liability:",

                    "TRAVEL WHEELS shall not be liable for any loss or damage to personal belongings left in the "
                    "vehicle during the rental period.",

                    "9. Cancellation Policy:",

                    "TRAVEL WHEELS reserves the right to cancel reservations due to unforeseen circumstances or  "
                    "vehicle unavailability.",

                    "10. Agreement to Terms:",
                    "By signing the rental agreement or accepting the terms online, the renter acknowledges and  "
                    "agrees to abide by these terms and conditions."
                ]

                def on_decline_click():  # if terms and conditions are declined
                    conditions_text.destroy()
                    conditions.destroy()

                def on_accept_click():  # if terms and conditions are accpeted
                    conditions_text.destroy()
                    conditions.destroy()
                    payment_option(booking_info_frame, customer_info_frame, car_info_frame)

                conditions = Listbox(window, bg='white', width=125, height=52, highlightthickness=0,
                                     borderwidth=2, highlightcolor='Black')
                conditions.place(x=470, y=80)

                label = Label(conditions, text='Terms And Conditions', bg='white', fg='Red',
                              font=("yu gothic ui bold", 19, 'bold'))
                label.place(relx=0.5, y=20, anchor='center')

                accept_button = Button(conditions, text='ACCEPT', fg='Black', bg='#1b87d2',
                                       font=("yu gothic ui bold", 16), cursor='hand2', command=on_accept_click)
                accept_button.place(x=399, y=765)

                decline_button = Button(conditions, text='DECLINE', fg='Black', highlightcolor='Blue', borderwidth=3,
                                        font=("yu gothic ui bold", 16), cursor='hand2', command=on_decline_click)
                decline_button.place(x=260, y=765)

                for _ in range(4):
                    conditions.insert(END, "")

                conditions_text = Text(window, bg='white', width=83, height=30, bd=2, relief='solid',
                                       font=("yu gothic ui", 13))
                conditions_text.place(x=471, y=130)

                # Add terms and conditions to the Text widget
                for condition in terms_and_conditions:
                    conditions_text.insert('end', condition + '\n')

            # Displays a payment successfull message
            def payment_successfull(payment_info_frame, booking_info_frame, customer_info_frame, car_info_frame):
                payment_status = Frame(window, bg='white', width=400, height=550, highlightthickness=3,
                                       borderwidth=3, highlightcolor='Black', highlightbackground='black')
                payment_status.place(x=600, y=310)

                image_path = "images/check.png"
                image = PhotoImage(file=image_path)

                # Create a Label to display the image
                image_label = Label(payment_status, image=image, bg="white")
                image_label.image = image  # Keep a reference to the image object
                image_label.place(relx=0.5, rely=0.2, anchor="center")

                label1 = Label(payment_status, text='Thank You!', bg='white', fg='#068a3a',
                               font=("yu gothic ui bold", 30, 'bold'))
                label1.place(x=99, y=220)
                label2 = Label(payment_status, text='Payment done Successfully', bg='white', fg='black',
                               font=("yu gothic ui bold", 19, 'bold'))
                label2.place(x=54, y=280)

                def rented_car_info(car_list):  # function to add car details that has been removed from the
                    # Cars_info table when the car has been rented
                    conn = sqlite3.connect("Car_Rental_Management_Database.db")
                    conn.execute(
                        "INSERT INTO Rented_car_list (Car_id, Car_no, Car_name, Seats_capacity, luggage_capacity,"
                        "transmission_type, fuel_type, car_type, vehicle_rent)"
                        "values (" + str(car_list[0][0]) + ",'" + car_list[0][1] + "','" + car_list[0][2] + "','" +
                        car_list[0][3] + "','" + car_list[0][4] + "','" + str(car_list[0][5]) + "','" + str(
                            car_list[0][6]) +
                        "','" + str(car_list[0][7]) + "','" + str(car_list[0][8]) + "'" ")")
                    # Insert_query to add car details to Rented_car_list table
                    print("Car list = ", car_list)
                    conn.commit()
                    conn.close()
                    car_history(car_list)

                def car_history(car_detail):
                    conn = sqlite3.connect("Car_Rental_Management_Database.db")
                    conn.execute('''INSERT INTO Car_history(Car_id, Car_name, Customer_name, Departure_date, 
                    Arrival_date, Revenue_generated) values(''' + str(car_detail[0][0]) + ",'" + car_detail[0][2] +
                                 "','" + order_details[9] + "','" + order_details[1] + "','" + order_details[2] + "'," +
                                 order_details[7] + ''')''')
                    # insert query to add history of the car to the Car_history table
                    conn.commit()
                    conn.close()
                    insert_rented_cars(car_detail)
                    remove_rented_car(car_detail[0][2])

                def insert_rented_cars(car_details1):
                    conn = sqlite3.connect("Car_Rental_Management_Database.db")
                    conn.execute('''INSERT INTO Rented_cars(Car_id, Car_no, Car_name, Customer_name, 
                    Customer_contact_number, Departure_date, Arrival_date) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                 (car_details1[0][0], car_details1[0][1], car_details1[0][2], order_details[9],
                                  order_details[8],
                                  order_details[1], order_details[2]))

                    # insert query to add history of the car to the Car_history table
                    conn.commit()
                    conn.close()

                def remove_rented_car(carname):
                    conn = sqlite3.connect("Car_Rental_Management_Database.db")
                    conn.execute("DELETE FROM Cars_info WHERE Car_name = ? ", (carname,))
                    conn.commit()
                    conn.close()

                def car_details():
                    con = sqlite3.connect("Car_Rental_Management_Database.db")
                    cursor = con.cursor()
                    cursor.execute("SELECT * FROM Cars_info WHERE Car_name = ?", (order_details[5],))
                    selected_car_info = cursor.fetchall()
                    rented_car_info(selected_car_info)

                def go_to_customer_frame():
                    payment_status.destroy()
                    payment_info_frame.destroy()
                    booking_info_frame.destroy()
                    customer_info_frame.destroy()
                    car_info_frame.destroy()
                    car_details()
                    order_details.clear()
                    clear_location_selection()
                    clear_time_selection()
                    print(order_details)

                home_button = Button(payment_status, text="HOME", fg='white', bg='#063638', width=10,
                                     font=("yu gothic ui bold", 16), cursor='hand2', command=go_to_customer_frame)
                home_button.place(x=120, y=420)

                def on_frame_click(event):
                    payment_status.focus_set()
                    payment_status.grab_set()

                payment_status.bind("<Button-1>", on_frame_click)

            # To make card Payment to book a car
            def card_payment_info(payment_info_frame, booking_info_frame, customer_info_frame, car_info_frame):
                def payment_status():
                    card_payment.destroy()
                    payment_successfull(payment_info_frame, booking_info_frame, customer_info_frame, car_info_frame)

                def check_entries_filled():  # to Check if all the entries are filled and valid or not
                    # Check if all entry fields are filled
                    if (name_entry.get() and number_entry.get() and cvv_entry.get() and month_combo.get() and
                            year_combo.get()):
                        # If all entries are filled, validate card number and CVV
                        validate_card = number_entry.get().replace(' ', '')  # Get card number without whitespace
                        validate_cvv = cvv_entry.get()

                        # Check if card number and CVV meet validation criteria
                        if len(validate_card) == 16 and validate_card.isdigit() and len(
                                validate_cvv) == 3 and validate_cvv.isdigit():
                            # If all conditions are met, call payment_status
                            payment_status()
                        else:
                            # Display appropriate error messages
                            if len(validate_card) != 16 or not validate_card.isdigit():
                                messagebox.showerror("Invalid Card Number",
                                                     "Please enter a valid 16-digit card number.")
                            elif len(validate_cvv) != 3 or not validate_cvv.isdigit():
                                messagebox.showerror("Invalid CVV", "Please enter a valid 3-digit CVV.")
                    else:
                        # Display message if any field is empty
                        messagebox.showerror("Empty Fields", "Please fill in all required fields.")

                card_payment = Frame(window, bg='white', width=830, height=500, highlightthickness=2,
                                     borderwidth=2, highlightcolor='Black')
                card_payment.place(x=400, y=330)

                image_path = "images/card.png"
                image = PhotoImage(file=image_path)

                # Create a Label to display the image
                image_label = Label(card_payment, image=image, bg="white")
                image_label.place(x=20, y=120)
                image_label.image = image

                label1 = Label(card_payment, text='Payment Details', fg='black', bg='white',
                               font=("yu gothic ui bold", 19, 'bold'))
                label1.place(x=490, y=20)

                label2 = Label(card_payment, text='Name on Card', fg='grey', bg='white',
                               font=("yu gothic ui bold", 16, 'bold'))
                label2.place(x=428, y=83)

                name_entry = Entry(card_payment, width=28, fg="black", font=("yu gothic ui semibold", 12),
                                   highlightthickness=2)
                name_entry.place(x=428, y=122)

                label3 = Label(card_payment, text='Card Number', fg='grey', bg='white',
                               font=("yu gothic ui bold", 16, 'bold'))
                label3.place(x=428, y=165)

                number_entry = Entry(card_payment, width=28, fg="black", font=("yu gothic ui semibold", 12),
                                     highlightthickness=2)
                number_entry.place(x=428, y=200)

                label4 = Label(card_payment, text='Expiration Date', fg='grey', bg='white',
                               font=("yu gothic ui bold", 16, 'bold'))
                label4.place(x=428, y=280)

                label5 = Label(card_payment, text='CVV', fg='grey', bg='white',
                               font=("yu gothic ui bold", 16, 'bold'))
                label5.place(x=680, y=280)

                cvv_entry = Entry(card_payment, width=7, fg="black", font=("yu gothic ui semibold", 12),
                                  highlightthickness=2)
                cvv_entry.place(x=680, y=325)

                proceed_button = Button(card_payment, text="PAY", fg='white', bg='#2fbd55', width=10,
                                        font=("yu gothic ui bold", 16), cursor='hand2')
                proceed_button.place(x=500, y=417)

                proceed_button['command'] = check_entries_filled

                def on_frame_click(event):
                    card_payment.focus_set()
                    card_payment.grab_set()

                card_payment.bind("<Button-1>", on_frame_click)

                months = [
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ]
                years = [str(year) for year in range(2027, 2037)]  # Convert integers to strings

                # Create ComboBoxes for days, months, and years
                month_combo = Combobox(card_payment, values=months, width=10, height=5)
                month_combo.place(x=428, y=330)
                year_combo = Combobox(card_payment, values=years, width=5, height=5)
                year_combo.place(x=545, y=330)

                # Set default values for the ComboBoxes
                month_combo.set('Month')
                year_combo.set('Year')

            # To make UPI payment to rent a car
            def upi_payment_info(payment_info_frame, booking_info_frame, customer_info_frame, car_info_frame):
                def payment_status():
                    upi_payment.destroy()
                    payment_successfull(payment_info_frame, booking_info_frame, customer_info_frame, car_info_frame)

                def check_entries_filled():  # To check if all entries are valid and filled
                    # Check if all entry fields are filled
                    if upi_id_entry.get():
                        # Check if UPI ID follows the specified format
                        upi_id = upi_id_entry.get()
                        if upi_id[0].isdigit() and '@' in upi_id:
                            # If all conditions are met, call payment_status
                            payment_status()
                        else:
                            # Display error message if the UPI ID format is incorrect
                            messagebox.showerror("Invalid UPI ID", "UPI ID must start with an integer followed by '@'.")
                    else:
                        # Display error message if any field is empty
                        messagebox.showerror("Empty Fields", "Please fill in all required fields.")

                upi_payment = Frame(window, bg='white', width=830, height=500, highlightthickness=2,
                                    borderwidth=2, highlightcolor='Black')
                upi_payment.place(x=400, y=410)

                image_path = "images/upi_payments.png"
                image = PhotoImage(file=image_path)

                # Create a Label to display the image
                image_label = Label(upi_payment, image=image, bg="white")
                image_label.place(x=20, y=120)
                image_label.image = image

                label = Label(upi_payment, text='Payment Details', fg='black', bg='white',
                              font=("yu gothic ui bold", 25, 'bold'))
                label.place(x=240, y=20)

                label1 = Label(upi_payment, text='Select your UPI app', bg='white', fg='#303436',
                               font=("yu gothic ui bold", 16, 'bold'))
                label1.place(x=472, y=130)

                label2 = Label(upi_payment, text='Enter your UPI id', bg='white', fg='#303436',
                               font=("yu gothic ui bold", 16, 'bold'))
                label2.place(x=472, y=252)

                upi_id_entry = Entry(upi_payment, width=17, fg="black", font=("yu gothic ui semibold", 12),
                                     highlightthickness=2)
                upi_id_entry.place(x=473, y=285)

                options = ["PhonePe", "GooglePay", "PayTm", "AmazonPay"]

                # Create a ComboBox
                combo_box = Combobox(upi_payment, values=options, width=14, height=5)
                combo_box.place(x=480, y=182)
                combo_box.configure(font=("Helvetica", 12))
                combo_box.set("Select an option")

                proceed_button = Button(upi_payment, text="PAY", fg='white', bg='#2fbd55', width=10,
                                        font=("yu gothic ui bold", 16), cursor='hand2')
                proceed_button.place(x=430, y=415)
                proceed_button['command'] = check_entries_filled

                def on_frame_click(event):
                    upi_payment.focus_set()
                    upi_payment.grab_set()

                upi_payment.bind("<Button-1>", on_frame_click)

            # To display the payment options to the customer
            def payment_option(booking_info_frame, customer_info_frame, car_info_frame):
                payment_info_frame = Frame(customer_frame, width=1600, height=600, background="#e4edf0")
                payment_info_frame.place(x=0, y=410)

                label1 = Label(payment_info_frame, text='PAYMENT METHODS', bg='#e4edf0', fg='purple',
                               font=("yu gothic ui bold", 21, 'bold'))
                label1.place(relx=0.5, y=20, anchor='center')

                label2 = Label(payment_info_frame, text='Choose an option to pay', bg='#e4edf0', fg='black',
                               font=("yu gothic ui bold", 21, 'bold'))
                label2.place(x=640, y=76)

                card_image_path = "images/card.png"
                card_image = PhotoImage(file=card_image_path)
                upi_image_path = "images/upi.png"
                upi_image = PhotoImage(file=upi_image_path)

                card_button = Button(payment_info_frame, image=card_image, compound="top", bg="#e4edf0",
                                     command=lambda: card_payment_info(payment_info_frame, booking_info_frame,
                                                                       customer_info_frame, car_info_frame),
                                     font=("arial", 18), borderwidth=0, cursor='hand2')
                card_button.place(x=400, y=180)
                card_button.image = card_image

                upi_button = Button(payment_info_frame, image=upi_image, compound="top", bg="#e4edf0",
                                    command=lambda: upi_payment_info(payment_info_frame, booking_info_frame,
                                                                     customer_info_frame, car_info_frame),
                                    font=("arial", 18), borderwidth=0, cursor='hand2')
                upi_button.place(x=880, y=180)
                upi_button.image = upi_image

            def customer_info(car_info_frame):  # To take the customer information for booking

                customer_info_frame = Frame(customer_frame, width=1600, height=600, background="#e4edf0")
                customer_info_frame.place(x=0, y=410)

                label = Label(customer_info_frame, text='CUSTOMER DETAILS', bg='#e4edf0', fg='Red',
                              font=("yu gothic ui bold", 21, 'bold'))
                label.place(relx=0.5, y=20, anchor='center')

                back_button = Button(customer_info_frame, text="Back", fg='Black', bg='#1b87d2', width=8,
                                     font=("yu gothic ui bold", 16), command=customer_info_frame.destroy)
                back_button.place(x=660, y=480)

                # Create labels and entry fields
                name = Label(customer_info_frame, text='Name: ', bg='#e4edf0', fg='Black',
                             font=("yu gothic ui bold", 17, 'bold'))
                name.place(x=80, y=70)

                name_entry = Entry(customer_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 12),
                                   highlightthickness=2)
                name_entry.place(x=280, y=75)

                age = Label(customer_info_frame, text='AGE : ', bg='#e4edf0', fg='Black',
                            font=("yu gothic ui bold", 17, 'bold'))
                age.place(x=80, y=140)
                age_entry = Entry(customer_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 12),
                                  highlightthickness=2)
                age_entry.place(x=280, y=145)

                contact = Label(customer_info_frame, text='Contact No. : ', bg='#e4edf0', fg='Black',
                                font=("yu gothic ui bold", 17, 'bold'))
                contact.place(x=80, y=210)
                contact_entry = Entry(customer_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 12),
                                      highlightthickness=2)
                contact_entry.place(x=280, y=215)

                email = Label(customer_info_frame, text='Email id : ', bg='#e4edf0', fg='Black',
                              font=("yu gothic ui bold", 17, 'bold'))
                email.place(x=80, y=280)
                email_entry = Entry(customer_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 12),
                                    highlightthickness=2)
                email_entry.place(x=280, y=285)

                address = Label(customer_info_frame, text='Address : ', bg='#e4edf0', fg='Black',
                                font=("yu gothic ui bold", 17, 'bold'))
                address.place(x=80, y=350)
                address_entry = Entry(customer_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 12),
                                      highlightthickness=2)
                address_entry.place(x=280, y=355)

                license_no = Label(customer_info_frame, text='License No. : ', bg='#e4edf0', fg='Black',
                                   font=("yu gothic ui bold", 17, 'bold'))
                license_no.place(x=80, y=420)
                license_no_entry = Entry(customer_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 12),
                                         highlightthickness=2)
                license_no_entry.place(x=280, y=425)

                emergency = Label(customer_info_frame, text='Emergency Contact : ', bg='#e4edf0', fg='Black',
                                  font=("yu gothic ui bold", 20, 'bold'))
                emergency.place(x=1010, y=70)

                person_name = Label(customer_info_frame, text='Name : ', bg='#e4edf0', fg='Black',
                                    font=("yu gothic ui bold", 17, 'bold'))
                person_name.place(x=880, y=140)
                person_name_entry = Entry(customer_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 12),
                                          highlightthickness=2)
                person_name_entry.place(x=1060, y=145)

                relation = Label(customer_info_frame, text='Relationship : ', bg='#e4edf0', fg='Black',
                                 font=("yu gothic ui bold", 17, 'bold'))
                relation.place(x=880, y=210)
                relation_entry = Entry(customer_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 12),
                                       highlightthickness=2)
                relation_entry.place(x=1060, y=215)

                emergency_contact_no = Label(customer_info_frame, text='Contact No. : ', bg='#e4edf0', fg='Black',
                                             font=("yu gothic ui bold", 17, 'bold'))
                emergency_contact_no.place(x=880, y=280)
                emergency_contact_no_entry = Entry(customer_info_frame, width=30, fg="black",
                                                   font=("yu gothic ui semibold", 12),
                                                   highlightthickness=2)
                emergency_contact_no_entry.place(x=1060, y=285)

                def handle_button_click(customer_name, customer_contact, customer_email, emergency_contact):
                    # Print values before appending to debug
                    print("Values before appending:", customer_name, customer_contact, customer_email,
                          emergency_contact)

                    pickup_date = order_details[0]  # Assuming the pickup date is at index 0
                    dropoff_date = order_details[2]  # Assuming the dropoff date is at index 2

                    # Convert the date strings to datetime objects
                    pickup_datetime = datetime.strptime(pickup_date, "%d-%m-%Y")
                    dropoff_datetime = datetime.strptime(dropoff_date, "%d-%m-%Y")

                    # Check if pickup and dropoff dates are the same
                    if pickup_datetime.date() == dropoff_datetime.date():
                        num_days_calculated = 1
                    else:
                        # Calculate the difference in days
                        difference = dropoff_datetime - pickup_datetime
                        num_days_calculated = difference.days

                    print(num_days_calculated)
                    order_details[3] = str(num_days_calculated)
                    print("Number of days difference (calculated):", num_days_calculated + 1)
                    print(order_details)

                    result = str(int(order_details[3]) * int(
                        order_details[6]))  # Calculate the result and convert it to a string
                    order_details.append(result)  # Append the result to the end of the list

                    print(order_details)

                    order_details.extend([customer_contact, customer_name, customer_email, emergency_contact])
                    check_entries_filled()

                def check_entries_filled():  # To check if all the entries are filled and valid
                    # List of all entry widgets
                    entry_widgets = [name_entry, age_entry, contact_entry, email_entry, address_entry,
                                     license_no_entry, person_name_entry, relation_entry, emergency_contact_no_entry]

                    # Check if any entry is empty
                    empty_entries = [entry for entry in entry_widgets if not entry.get()]

                    # If any entry is empty, display a messagebox
                    if empty_entries:
                        messagebox.showerror("Empty Fields", "Please fill in all required fields.")
                    else:
                        # Check if age is 21 or older
                        age = age_entry.get()
                        if not age.isdigit() or int(age) < 21:
                            messagebox.showerror("Age Requirement", "You must be 21 years or older to rent a car.")
                        else:
                            # Check if contact_entry consists of only 10 integers
                            contact = contact_entry.get()
                            if not (contact.isdigit() and len(contact) == 10):
                                messagebox.showerror("Invalid Contact Number",
                                                     "Contact number must consist of exactly 10 digits.")
                            else:
                                # Check if emergency_contact_no_entry consists of only 10 integers
                                emergency_contact = emergency_contact_no_entry.get()
                                if not (emergency_contact.isdigit() and len(emergency_contact) == 10):
                                    messagebox.showerror("Invalid Emergency Contact Number",
                                                         "Emergency contact number must consist of exactly 10 digits.")
                                elif contact == emergency_contact:
                                    messagebox.showerror("Same Contacts",
                                                         "Contact number and emergency contact number cannot be the "
                                                         "same.")
                                else:
                                    # Check if email_entry is valid
                                    email = email_entry.get()
                                    if not ("@" in email and email.endswith(".com")):
                                        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
                                    else:
                                        '''filled = 0
                                        while filled != 1:
                                            filled = check_date_time()'''
                                        booking_info(customer_info_frame, car_info_frame)

                proceed_button = Button(customer_info_frame, text="Proceed", fg='Black', bg='#1b87d2',
                                        font=("yu gothic ui bold", 16),
                                        command=lambda: handle_button_click(name_entry.get(), contact_entry.get(),
                                                                            email_entry.get(),
                                                                            emergency_contact_no_entry.get()))

                proceed_button.place(x=840, y=480)
                print(order_details)

            def booking_info(customer_info_frame, car_info_frame):  # To diplay the booking details
                booking_info_frame = Frame(customer_frame, width=1600, height=600, background="#e4edf0")
                booking_info_frame.place(x=0, y=410)
                print(order_details)

                pay_button = Button(booking_info_frame, text="PAY", fg='Black', bg='#1b87d2', width=8,
                                    font=("yu gothic ui bold", 16),
                                    command=lambda: terms_and_conditions(booking_info_frame, customer_info_frame,
                                                                         car_info_frame))
                pay_button.place(x=840, y=490)

                back_button = Button(booking_info_frame, text="BACK", fg='Black', bg='#1b87d2', width=8,
                                     font=("yu gothic ui bold", 16), command=booking_info_frame.destroy)
                back_button.place(x=660, y=490)

                label = Label(booking_info_frame, text='BOOKING DETAILS', bg='#e4edf0', fg='Red',
                              font=("yu gothic ui bold", 21, 'bold'))
                label.place(relx=0.5, y=20, anchor='center')

                name = Label(booking_info_frame, text='Car Name: ', bg='#e4edf0', fg='Black',
                             font=("yu gothic ui bold", 17, 'bold'))
                name.place(x=80, y=70)

                name_detail = Label(booking_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 14),
                                    highlightthickness=2, text=order_details[5])
                name_detail.place(x=340, y=75)

                pickup = Label(booking_info_frame, text='Pick-up Date : ', bg='#e4edf0', fg='Black',
                               font=("yu gothic ui bold", 17, 'bold'))
                pickup.place(x=80, y=140)
                pickup_detail = Label(booking_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 14),
                                      highlightthickness=2, text=order_details[0])
                pickup_detail.place(x=340, y=145)

                dropoff = Label(booking_info_frame, text='Drop-off Date. : ', bg='#e4edf0', fg='Black',
                                font=("yu gothic ui bold", 17, 'bold'))
                dropoff.place(x=80, y=210)
                dropoff_detail = Label(booking_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 14),
                                       highlightthickness=2, text=order_details[2])
                dropoff_detail.place(x=340, y=215)

                pick_up1 = Label(booking_info_frame, text='Pick-up Location : ', bg='#e4edf0', fg='Black',
                                 font=("yu gothic ui bold", 17, 'bold'))
                pick_up1.place(x=80, y=280)
                pick_up1 = Label(booking_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 14),
                                 highlightthickness=2, text=order_details[4])
                pick_up1.place(x=340, y=285)

                total_days = Label(booking_info_frame, text='Rent Duration : ', bg='#e4edf0', fg='Black',
                                   font=("yu gothic ui bold", 17, 'bold'))
                total_days.place(x=80, y=350)
                total_days = Label(booking_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 14),
                                   highlightthickness=2, text=str(order_details[3]) + " Days")
                total_days.place(x=340, y=355)

                customer_name = Label(booking_info_frame, text='Name  : ', bg='#e4edf0', fg='Black',
                                      font=("yu gothic ui bold", 17, 'bold'))
                customer_name.place(x=880, y=70)
                customer_name_detail = Label(booking_info_frame, width=30, fg="black",
                                             font=("yu gothic ui semibold", 14),
                                             highlightthickness=2, text=order_details[9])
                customer_name_detail.place(x=1170, y=75)

                customer_number = Label(booking_info_frame, text='Contact No. : ', bg='#e4edf0', fg='Black',
                                        font=("yu gothic ui bold", 17, 'bold'))
                customer_number.place(x=880, y=140)
                customer_number_detail = Label(booking_info_frame, width=30, fg="black",
                                               font=("yu gothic ui semibold", 14),
                                               highlightthickness=2, text=order_details[8])
                customer_number_detail.place(x=1170, y=145)

                email = Label(booking_info_frame, text='Email id : ', bg='#e4edf0', fg='Black',
                              font=("yu gothic ui bold", 17, 'bold'))
                email.place(x=880, y=210)
                email_detail = Label(booking_info_frame, width=30, fg="black", font=("yu gothic ui semibold", 14),
                                     highlightthickness=2, text=order_details[10])
                email_detail.place(x=1170, y=215)

                emergency_contact_no = Label(booking_info_frame, text='Emergency Contact : ', bg='#e4edf0', fg='Black',
                                             font=("yu gothic ui bold", 17, 'bold'))
                emergency_contact_no.place(x=880, y=280)
                emergency_contact_detail = Label(booking_info_frame, width=30, fg="black",
                                                 font=("yu gothic ui semibold", 14),
                                                 highlightthickness=2, text=order_details[11])
                emergency_contact_detail.place(x=1170, y=285)

                total_rent = Label(booking_info_frame, text='Total Rent : ', bg='#e4edf0', fg='Black',
                                   font=("yu gothic ui bold", 17, 'bold'))
                total_rent.place(x=880, y=365)
                total_rent = Label(booking_info_frame, width=30, fg="black",
                                   font=("yu gothic ui semibold", 14),
                                   highlightthickness=2, text="Rs " + order_details[7])
                total_rent.place(x=1170, y=370)

            # to create a frame related to Specifc Car information and formal parameters are the details
            # of the car
            def create_car_info_frame(parent_frame, car_name, car_type, seat_capacity, luggage_capacity, fan_type,
                                      transmission_type, fuel_type, rent_price, car_image_path, car_type_image):
                def search_car(car):
                    # Connect to the database
                    conn = sqlite3.connect('Car_Rental_Management_Database.db')
                    cursor = conn.cursor()
                    print(car)
                    # Execute the SQL query to check if the car exists
                    cursor.execute("SELECT * FROM Cars_info WHERE car_name = ?", (car,))
                    result = cursor.fetchone()
                    print(result)
                    conn.close()  # Close the connection

                    if result is None:
                        messagebox.showinfo("Car Not Found", "Sorry, the car you want to rent isn't"
                                                             " available. Please choose another option.")
                        print("car not available")
                    else:
                        customer_info(car_info_frame)
                        order_details.append(car_name)
                        order_details.append(rent_price)

                car_info_frame = Frame(parent_frame, width=1600, height=600, background="#013b4d")
                car_info_frame.place(x=0, y=410)

                design_frame = Listbox(car_info_frame, bg='#e4edf0', width=150, height=38, highlightthickness=0,
                                       borderwidth=1)
                design_frame.place(x=656, y=0)

                image1 = PhotoImage(file=car_type_image)
                image_label = Label(design_frame, image=image1, background='#e4edf0', bd=0)
                image_label.place(x=50, y=50, width=70, height=64)
                image_label.image = image1
                car_type_label = Label(design_frame, bg='#e4edf0', text=car_type, font=("Helvetica", 18))
                car_type_label.place(x=160, y=66)

                seat_image = PhotoImage(file="images/seats.png")
                seat_image_label = Label(design_frame, image=seat_image, background='#e4edf0', bd=0)
                seat_image_label.place(x=50, y=180, width=70, height=68)
                seat_image_label.image = seat_image
                seat_capacity_label = Label(design_frame, bg='#e4edf0', text=seat_capacity, font=("Helvetica", 18))
                seat_capacity_label.place(x=160, y=194)

                luggage_image = PhotoImage(file="images/luggage.png")
                luggage_image_label = Label(design_frame, image=luggage_image, background='#e4edf0', bd=0)
                luggage_image_label.place(x=50, y=310, width=70, height=68)
                luggage_image_label.image = luggage_image
                luggage_type_label = Label(design_frame, bg='#e4edf0', text=luggage_capacity, font=("Helvetica", 18))
                luggage_type_label.place(x=160, y=322)

                fan_image = PhotoImage(file="images/fan.png")
                fan_image_label = Label(design_frame, image=fan_image, background='#e4edf0', bd=0)
                fan_image_label.place(x=450, y=50, width=70, height=68)
                fan_image_label.image = fan_image
                fan_type_label = Label(design_frame, bg='#e4edf0', text=fan_type, font=("Helvetica", 18))
                fan_type_label.place(x=590, y=66)

                transmission_image = PhotoImage(file="images/transmission.png")
                transmission_image_label = Label(design_frame, image=transmission_image, background='#e4edf0', bd=0)
                transmission_image_label.place(x=450, y=180, width=70, height=68)
                transmission_image_label.image = transmission_image
                transmission_type_label = Label(design_frame, bg='#e4edf0', text=transmission_type,
                                                font=("Helvetica", 18))
                transmission_type_label.place(x=590, y=194)

                fuel_image = PhotoImage(file="images/fuel.png")
                fuel_image_label = Label(design_frame, image=fuel_image, background='#e4edf0', bd=0)
                fuel_image_label.place(x=450, y=310, width=70, height=68)
                fuel_image_label.image = fuel_image
                fuel_type_label = Label(design_frame, bg='#e4edf0', text=fuel_type, font=("Helvetica", 18))
                fuel_type_label.place(x=590, y=322)

                image2 = PhotoImage(file=car_image_path)
                image_label2 = Label(design_frame, image=image2, background='#e4edf0', bd=0)

                image_label2 = Label(car_info_frame, image=image2, background='#e4edf0', bd=3, relief="solid")
                image_label2.image = image2

                image_label2.place(x=80, y=40, width=450, height=320)

                if car_name == 'MARUTI SWIFT' or car_name == 'HYUNDAI VIRTUS':
                    text_label = Label(car_info_frame, text=car_name, background='#013b4d', fg='white',
                                       font=("arial", 19, "bold"))
                    text_label.place(x=173, y=390)
                elif car_name == 'SUZUKI CIAZ' or car_name == 'TATA SAFARI':
                    text_label = Label(car_info_frame, text=car_name, background='#013b4d', fg='white',
                                       font=("arial", 19, "bold"))
                    text_label.place(x=192, y=390)
                else:
                    text_label = Label(car_info_frame, text=car_name, background='#013b4d', fg='white',
                                       font=("arial", 19, "bold"))
                    text_label.place(x=170, y=390)

                rent_price_label = Label(car_info_frame, bg='#013b4d', text="Rs " + str(rent_price), font=("Helvetica",
                                                                                                           19),
                                         fg='white')
                rent_price_label.place(x=215, y=440)

                book_button = Button(car_info_frame, fg='Black', text='Book Car', bg='#1b87d2',
                                     font=("yu gothic ui bold", 16), cursor='hand2',
                                     command=lambda: search_car(car_name))
                book_button.place(x=1100, y=480)

                back_button1 = Button(car_info_frame, fg='Black', text='Back', bg='#1b87d2', width=8,
                                      font=("yu gothic ui bold", 16), cursor='hand2', command=car_info_frame.destroy)
                back_button1.place(x=960, y=480)

                conn = sqlite3.connect('Car_Rental_Management_Database.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Cars_info WHERE Car_name = ?", (new_car_name,))
                rows = cursor.fetchall()

                # Close the cursor and connection
                cursor.close()
                conn.close()

            def breeza_info():
                create_car_info_frame(customer_frame, "MARUTI BREEZA", "Hatchback", "4 Adults", "2 Bags", "AC",
                                      "Automatic", "Diesel", "4499", "images/breeza.png", "images/car_symbol.png")

            def swift_info():
                create_car_info_frame(customer_frame, "MARUTI SWIFT", "Hatchback", "4 Adults", "2 Bags", "AC",
                                      "Manual", "Diesel", "3999", "images/swift1.png", "images/car_symbol.png")

            def virtus_info():
                create_car_info_frame(customer_frame, "HYUNDAI VIRTUS", "Sedan", "4 Adults", "2 Bags", "AC",
                                      "Automatic", "Petrol", "6599", "images/virtus1.png", "images/car_symbol.png")

            def innova_info():
                create_car_info_frame(customer_frame, "TOYOTA INNOVA", "SUV", "5 Adults", "3 Bags", "AC",
                                      "Manual", "Diesel", "7499", "images/innova1.png", "images/car_symbol.png")

            def scorpio_info():
                create_car_info_frame(customer_frame, "MAHINDRA SCORPIO", "SUV", "5 Adults", "4 Bags", "AC",
                                      "Manual", "Diesel", "8499", "images/scorpio1.png", "images/car_symbol.png")

            def traveller_info():
                create_car_info_frame(customer_frame, "FORCE TRAVELLER", "Mini Bus", "10 Adults", "6 Bags", "AC",
                                      "Manual", "Diesel", "14999", "images/traveller1.png", "images/car_symbol.png")

            def ciaz_info():
                create_car_info_frame(customer_frame, "SUZUKI CIAZ", "Sedan", "4 Adults", "3 Bags", "AC",
                                      "Automatic", "Petrol", "6999", "images/ciaz1.png", "images/car_symbol.png")

            def safari_info():
                create_car_info_frame(customer_frame, "TATA SAFARI", "SUV", "5 Adults", "4 Bags", "AC",
                                      "Manual", "Diesel", "7999", "images/safari1.png", "images/car_symbol.png")

            def creta_info():
                create_car_info_frame(customer_frame, "HYUNDAI CRETA", "SUV", "5 Adults", "2 Bags", "AC",
                                      "Manual", "Diesel", "5499", "new_cars/creta.png", "images/car_symbol.png")

            def car_info(vehicle_name, image_path):
                # Connect to the database
                conn = sqlite3.connect('Car_Rental_Management_Database.db')
                cursor = conn.cursor()
                print(vehicle_name)

                # Check if car_name exists
                cursor.execute("SELECT * FROM Cars_info WHERE car_name = ?", (vehicle_name,))
                vehicle_details = cursor.fetchone()

                conn.commit()
                cursor.close()
                conn.close()
                print(vehicle_details)
                create_car_info_frame(customer_frame, vehicle_name, vehicle_details[7], vehicle_details[3],
                                      vehicle_details[4], "AC", vehicle_details[5], vehicle_details[6],
                                      vehicle_details[8], image_path, "images/car_symbol.png")

            # Display image buttons for cars
            def popular_cars():  # to display all the popular cars to the customer interface
                with open("car_data.txt", "r") as file:
                    existing_data = file.read()

                if "car1" not in existing_data:
                    # Additional dictionary to store car data
                    car_dict = {
                        "car1": "MARUTI BREEZA",
                        "car2": "MARUTI SWIFT",
                        "car3": "HYUNDAI VIRTUS",
                        "car4": "TOYOTA INNOVA",
                        "car5": "MAHINDRA SCORPIO",
                        "car6": "FORCE TRAVELLER",
                        "car7": "SUZUKI CIAZ",
                        "car8": "HYUNDAI CRETA"
                    }

                    # Append the car_dict to the file
                    with open(file_name, "a") as file:
                        file.write("\n")  # Add a newline separator
                        for key, value in car_dict.items():
                            file.write(f"{key}: {value}\n")

                    print("Dictionary saved to 'car_data.txt' file.")
                else:
                    print("Dictionary data already exists in 'car_data.txt' file. Skipping appending.")

                # Open the file
                with open('car_data.txt', 'r') as file:
                    # Read lines from the file
                    lines = file.readlines()

                # Initialize lists to store values of old_car, new_car, and new_car_path

                # Loop through the lines and extract the values for old_car, new_car, and new_car_path
                for line in lines:
                    if line.startswith('old_car@'):
                        value = line.split(': ')[1].strip()
                        old_car_values.append(int(value) if value else None)
                    elif line.startswith('car'):
                        value = line.split(': ')[1].strip()
                        car_names.append(str(value) if value else None)
                    elif line.startswith('new_car@'):
                        value = line.split(': ')[1].strip()
                        new_car_values.append(int(value) if value else None)
                    elif line.startswith('new_car_path'):
                        split_line = line.split(': ')
                        if len(split_line) > 1:  # Check if there's at least one element after splitting
                            new_car_path_values.append(split_line[1].strip())
                        else:
                            new_car_path_values.append('')  # Append an empty string if no value found

                # Print the lists
                print("Values of carX:", car_names)
                print("Values of old_car@X:", old_car_values)
                print("Values of new_car@X:", new_car_values)
                print("Values of new_car_pathX:", new_car_path_values)
                print("\nValues have been added 1st time\n")

                if old_car_values[0] == 1 and new_car_values[0] == 1:
                    # Create a new image button with the image from new_car_path_values[0]
                    new_image_path = new_car_path_values[0]
                    new_image = PhotoImage(file=new_image_path)
                    car_button = Button(new_frame, image=new_image, compound="top", bg="#daebf0",
                                        command=lambda: car_info(car_names[0], new_car_path_values[0]), relief="solid",
                                        cursor='hand2', text=car_names[0], font=("arial", 16), borderwidth=3)
                    car_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                    car_button.pack()
                    car_button.place(x=40, y=52, width=288, height=205)
                else:
                    car1_image = PhotoImage(file="images/breeza1.png")
                    car_button = Button(new_frame, image=car1_image, compound="top", bg="#daebf0",
                                        command=breeza_info, relief="solid", cursor='hand2', text="Maruti Breeza",
                                        font=("arial", 16), borderwidth=3)
                    car_button.image = car1_image
                    car_button.place(x=40, y=52, width=288, height=205)

                if old_car_values[1] == 1 and new_car_values[1] == 1:
                    new_image_path = new_car_path_values[1]
                    new_image = PhotoImage(file=new_image_path)
                    car_button = Button(new_frame, image=new_image, compound="top", bg="#daebf0",
                                        command=lambda: car_info(car_names[1], new_car_path_values[1]), relief="solid",
                                        cursor='hand2', text=car_names[1], font=("arial", 16), borderwidth=3)
                    car_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                    car_button.pack()
                    car_button.place(x=415, y=52, width=288, height=205)
                else:
                    car1_image = PhotoImage(file="images/swift.png")
                    car_button = Button(new_frame, image=car1_image, compound="top", bg="#daebf0",
                                        command=swift_info, relief="solid", cursor='hand2', text="Maruti Swift",
                                        font=("arial", 16), borderwidth=3)
                    car_button.image = car1_image
                    car_button.place(x=415, y=52, width=288, height=205)

                if old_car_values[2] == 1 and new_car_values[2] == 1:
                    new_image_path = new_car_path_values[2]
                    new_image = PhotoImage(file=new_image_path)
                    car_button = Button(new_frame, image=new_image, compound="top", bg="#daebf0",
                                        command=lambda: car_info(car_names[2], new_car_path_values[2]), relief="solid",
                                        cursor='hand2', text=car_names[2], font=("arial", 16), borderwidth=3)
                    car_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                    car_button.pack()
                    car_button.place(x=810, y=52, width=288, height=205)
                else:
                    car1_image = PhotoImage(file="images/virtus.png")
                    car_button = Button(new_frame, image=car1_image, compound="top", bg="#daebf0",
                                        command=virtus_info, relief="solid", cursor='hand2', text="Hyundai Virtus",
                                        font=("arial", 16), borderwidth=3)
                    car_button.image = car1_image
                    car_button.place(x=810, y=52, width=288, height=205)

                if old_car_values[3] == 1 and new_car_values[3] == 1:
                    new_image_path = new_car_path_values[3]
                    new_image = PhotoImage(file=new_image_path)
                    car_button = Button(new_frame, image=new_image, compound="top", bg="#daebf0",
                                        command=lambda: car_info(car_names[3], new_car_path_values[3]), relief="solid",
                                        cursor='hand2', text=car_names[3], font=("arial", 16), borderwidth=3)
                    car_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                    car_button.pack()
                    car_button.place(x=1200, y=52, width=288, height=205)
                else:
                    car1_image = PhotoImage(file="images/ciaz.png")
                    car_button = Button(new_frame, image=car1_image, compound="top", bg="#daebf0",
                                        command=ciaz_info, relief="solid", cursor='hand2', text="Hyundai Ciaz",
                                        font=("arial", 16), borderwidth=3)
                    car_button.image = car1_image
                    car_button.place(x=1200, y=52, width=288, height=205)

                if old_car_values[4] == 1 and new_car_values[4] == 1:
                    new_image_path = new_car_path_values[4]
                    new_image = PhotoImage(file=new_image_path)
                    car_button = Button(new_frame, image=new_image, compound="top", bg="#daebf0",
                                        command=lambda: car_info(car_names[4], new_car_path_values[4]), relief="solid",
                                        cursor='hand2', text=car_names[4], font=("arial", 16), borderwidth=3)
                    car_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                    car_button.pack()
                    car_button.place(x=40, y=280, width=288, height=205)
                else:
                    car1_image = PhotoImage(file="images/innova.png")
                    car_button = Button(new_frame, image=car1_image, compound="top", bg="#daebf0",
                                        command=innova_info, relief="solid", cursor='hand2', text="Toyota Innova",
                                        font=("arial", 16), borderwidth=3)
                    car_button.image = car1_image
                    car_button.place(x=40, y=280, width=288, height=205)

                if old_car_values[5] == 1 and new_car_values[5] == 1:
                    new_image_path = new_car_path_values[5]
                    new_image = PhotoImage(file=new_image_path)
                    car_button = Button(new_frame, image=new_image, compound="top", bg="#daebf0",
                                        command=lambda: car_info(car_names[5], new_car_path_values[5]), relief="solid",
                                        cursor='hand2', text=car_names[5], font=("arial", 16), borderwidth=3)
                    car_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                    car_button.pack()
                    car_button.place(x=415, y=280, width=288, height=205)
                else:
                    car1_image = PhotoImage(file="images/scorpio.png")
                    car_button = Button(new_frame, image=car1_image, compound="top", bg="#daebf0",
                                        command=scorpio_info, relief="solid", cursor='hand2', text="Mahindra Scorpio",
                                        font=("arial", 16), borderwidth=3)
                    car_button.image = car1_image
                    car_button.place(x=415, y=280, width=288, height=205)

                if old_car_values[6] == 1 and new_car_values[6] == 1:
                    new_image_path = new_car_path_values[6]
                    new_image = PhotoImage(file=new_image_path)
                    car_button = Button(new_frame, image=new_image, compound="top", bg="#daebf0",
                                        command=lambda: car_info(car_names[6], new_car_path_values[6]), relief="solid",
                                        cursor='hand2', text=car_names[6], font=("arial", 16), borderwidth=3)
                    car_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                    car_button.pack()
                    car_button.place(x=810, y=280, width=288, height=205)
                else:
                    car1_image = PhotoImage(file="images/traveller.png")
                    car_button = Button(new_frame, image=car1_image, compound="top", bg="#daebf0",
                                        command=traveller_info, relief="solid", cursor='hand2', text="Force Traveller",
                                        font=("arial", 16), borderwidth=3)
                    car_button.image = car1_image
                    car_button.place(x=810, y=280, width=288, height=205)

                if old_car_values[7] == 1 and new_car_values[7] == 1:
                    new_image_path = new_car_path_values[7]
                    new_image = PhotoImage(file=new_image_path)
                    car_button = Button(new_frame, image=new_image, compound="top", bg="#daebf0",
                                        command=lambda: car_info(car_names[7], new_car_path_values[7]), relief="solid",
                                        cursor='hand2', text=car_names[7], font=("arial", 16), borderwidth=3)
                    car_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                    car_button.pack()
                    car_button.place(x=810, y=280, width=288, height=205)
                else:
                    car1_image = PhotoImage(file="images/safari.png")
                    car_button = Button(new_frame, image=car1_image, compound="top", bg="#daebf0",
                                        command=safari_info, relief="solid", cursor='hand2', text="Tata Safari",
                                        font=("arial", 16), borderwidth=3)
                    car_button.image = car1_image
                    car_button.place(x=1200, y=280, width=288, height=205)

                close_button = Button(customer_frame, text="Close Window", fg='white', bg='Red',
                                      font=("yu gothic ui bold", 16), cursor='hand2', command=close_window)
                close_button.place(x=30, y=30)

                def all_cars_2():
                    # Open the file
                    with open('car_data2.txt', 'r') as file:
                        # Read lines from the file
                        lines = file.readlines()

                    car_names2 = []
                    old_car_values2 = []
                    new_car_values2 = []
                    new_car_path_values2 = []

                    # Initialize lists to store values of old_car, new_car, and new_car_path

                    # Loop through the lines and extract the values for old_car, new_car, and new_car_path
                    for line in lines:
                        if line.startswith('old_car@'):
                            value = line.split(': ')[1].strip()
                            old_car_values2.append(int(value) if value else None)
                        elif line.startswith('car'):
                            value = line.split(': ')[1].strip()
                            car_names2.append(str(value) if value else None)
                        elif line.startswith('new_car@'):
                            value = line.split(': ')[1].strip()
                            new_car_values2.append(int(value) if value else None)
                        elif line.startswith('new_car_path'):
                            split_line = line.split(': ')
                            if len(split_line) > 1:  # Check if there's at least one element after splitting
                                new_car_path_values2.append(split_line[1].strip())
                            else:
                                new_car_path_values2.append('')  # Append an empty string if no value found

                    # Print the lists
                    print("Values of carX:", car_names)
                    print("Values of old_car@X:", old_car_values)
                    print("Values of new_car@X:", new_car_values)
                    print("Values of new_car_pathX:", new_car_path_values)
                    print("\nValues have been added 1st time\n")

                    all_cars_frame2 = Frame(customer_frame, width=1600, height=600, background="#daebf0")
                    all_cars_frame2.place(x=0, y=410)

                    if old_car_values[8] == 1 and new_car_values[8] == 1:
                        # Create a new image button with the image from new_car_path_values[0]
                        new_image_path = new_car_path_values[8]
                        new_image = PhotoImage(file=new_image_path)
                        car9_button = Button(all_cars_frame2, image=new_image, compound="top", bg="#daebf0",
                                             command=lambda: car_info(car_names[8], new_car_path_values[8]),
                                             relief="solid", cursor='hand2', text=car_names[8], font=("arial", 16),
                                             borderwidth=3)
                        car9_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                        car9_button.pack()
                    else:
                        creta_image = PhotoImage(file="new_cars/creta1.png")
                        car9_button = Button(all_cars_frame2, image=creta_image, compound="top", bg="#daebf0",
                                             text="Creta", font=("arial", 16), relief="solid", cursor='hand2',
                                             borderwidth=3, command=creta_info)
                        car9_button.image = creta_image
                        car9_button.place(x=40, y=50, width=288, height=205)

                    if new_car_values2[0] != 0:
                        # Create a new image button with the image from new_car_path_values[0]
                        new_image_path = new_car_path_values2[0]
                        new_image = PhotoImage(file=new_image_path)
                        car10_button = Button(all_cars_frame2, image=new_image, compound="top", bg="#daebf0",
                                              command=lambda: car_info(car_names2[0], new_car_path_values2[0]),
                                              relief="solid", cursor='hand2', text=car_names2[0], font=("arial", 16),
                                              borderwidth=3)
                        car10_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                        car10_button.place(x=415, y=50, width=288, height=205)

                    if new_car_values2[1] != 0:
                        # Create a new image button with the image from new_car_path_values[0]
                        new_image_path = new_car_path_values2[1]
                        new_image = PhotoImage(file=new_image_path)
                        car11_button = Button(all_cars_frame2, image=new_image, compound="top", bg="#daebf0",
                                              command=lambda: car_info(car_names2[1], new_car_path_values2[1]),
                                              relief="solid", cursor='hand2', text=car_names2[1], font=("arial", 16),
                                              borderwidth=3)
                        car11_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                        car11_button.place(x=810, y=50, width=288, height=205)

                    if new_car_values2[2] != 0:
                        # Create a new image button with the image from new_car_path_values[0]
                        new_image_path = new_car_path_values2[11]
                        new_image = PhotoImage(file=new_image_path)
                        car12_button = Button(all_cars_frame2, image=new_image, compound="top", bg="#daebf0",
                                              command=lambda: car_info(car_names2[2], new_car_path_values2[2]),
                                              relief="solid", cursor='hand2', text=car_names2[2], font=("arial", 16),
                                              borderwidth=3)
                        car12_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                        car12_button.place(x=1200, y=50, width=288, height=205)

                    if new_car_values2[3] != 0:
                        # Create a new image button with the image from new_car_path_values[0]
                        new_image_path = new_car_path_values2[3]
                        new_image = PhotoImage(file=new_image_path)
                        car13_button = Button(all_cars_frame2, image=new_image, compound="top", bg="#daebf0",
                                              command=lambda: car_info(car_names2[3], new_car_path_values2[3]),
                                              relief="solid", cursor='hand2', text=car_names2[3], font=("arial", 16),
                                              borderwidth=3)
                        car13_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                        car13_button.place(x=40, y=275, width=288, height=205)

                    if new_car_values2[4] != 0:
                        # Create a new image button with the image from new_car_path_values[0]
                        new_image_path = new_car_path_values2[4]
                        new_image = PhotoImage(file=new_image_path)
                        car14_button = Button(all_cars_frame2, image=new_image, compound="top", bg="#daebf0",
                                              command=lambda: car_info(car_names2[4], new_car_path_values2[4]),
                                              relief="solid", cursor='hand2', text=car_names2[4], font=("arial", 16),
                                              borderwidth=3)
                        car14_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                        car14_button.place(x=415, y=275, width=288, height=205)

                    if new_car_values2[5] != 0:
                        # Create a new image button with the image from new_car_path_values[0]
                        new_image_path = new_car_path_values2[5]
                        new_image = PhotoImage(file=new_image_path)
                        car15_button = Button(all_cars_frame2, image=new_image, compound="top", bg="#daebf0",
                                              command=lambda: car_info(car_names2[5], new_car_path_values2[5]),
                                              relief="solid", cursor='hand2', text=car_names2[5], font=("arial", 16),
                                              borderwidth=3)
                        car15_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                        car15_button.place(x=810, y=50, width=288, height=205)

                    if new_car_values2[6] != 0:
                        # Create a new image button with the image from new_car_path_values[0]
                        new_image_path = new_car_path_values2[6]
                        new_image = PhotoImage(file=new_image_path)
                        car10_button = Button(all_cars_frame2, image=new_image, compound="top", bg="#daebf0",
                                              command=lambda: car_info(car_names2[6], new_car_path_values2[6]),
                                              relief="solid", cursor='hand2', text=car_names2[6], font=("arial", 16),
                                              borderwidth=3)
                        car10_button.image = new_image  # Keep a reference to the image to prevent garbage collection
                        car10_button.place(x=1200, y=50, width=288, height=205)

                    next_button = Button(all_cars_frame2, fg='Black', text='Previous', bg='#1b87d2', width=9,
                                         font=("yu gothic ui bold", 16), cursor='hand2',
                                         command=all_cars_frame2.destroy)
                    next_button.place(x=700, y=485)

                next_button = Button(customer_frame, fg='Black', text='Next', bg='#1b87d2', width=8,
                                     font=("yu gothic ui bold", 16), cursor='hand2', command=all_cars_2)
                next_button.place(x=710, y=905)

                def all_cars():  # function to display all cars in the system to the Customer
                    all_cars_frame = Frame(customer_frame, width=1600, height=600, background="#daebf0")
                    all_cars_frame.place(x=0, y=410)

            popular_cars()

            # Hide other frames
            if frame1 is not None:
                frame1.pack_forget()
            if frame2 is not None:
                frame2.pack_forget()
            customer_frame.pack(fill="both", expand=True)

    def admin_clicked():  # to check valid username and password
        def login(username, password):
            # Get the entered username and password
            # Check if the username and password match
            if username == "" and password == "":
                result = messagebox.askokcancel("Login", "Login successful!")
                if result:
                    userid.delete(0, END)
                    password_entry2.delete(0, END)
                    admin_dashboard()
            else:
                messagebox.showerror("Login", "Incorrect username or password.")

        global admin_frame
        if admin_frame is None:
            admin_frame = Frame(window, bg="black", width=900, height=900)
            admin_frame.place(x=0, y=0)

            def admin_dashboard():  # function to display the admin Dashboard
                def logout():  # function to display a messagebox related to log out
                    result = messagebox.askyesno("Logout", "Are you sure you want to Logout?")
                    if result:
                        admin_main_dashframe.destroy()

                        # Move back to previous frame or perform logout action
                        print("Logging out...")
                    else:
                        # Stay on the current frame
                        print("Cancelled logout")

                admin_main_dashframe = Frame(admin_frame, bg="black", width=1600, height=1000)
                admin_main_dashframe.place(x=0, y=0)

                rental_name = Label(admin_main_dashframe, text="Welcome to Travel Wheels",
                                    font=("Helvetica", 40, "bold"), fg="white", bg="#2b184d", width=62, height=3,
                                    anchor="center", justify="center")
                rental_name.place(relx=0.5, rely=0.07, anchor="center")

                menu_label = Label(admin_main_dashframe, width=300, height=10, bg='pink')
                menu_label.place(x=0, y=150)

                def add_cars():  # to add cars in the system
                    def select_image():
                        global new_image_path
                        new_image_path = filedialog.askopenfilename()
                        print("THE IMAGE PATH = ", new_image_path)

                    add_cars_frame = Frame(admin_main_dashframe, width=1600, height=700, background="#4e4f4f")
                    add_cars_frame.place(x=0, y=310)

                    add_car_icon = PhotoImage(file="images/new_car.png")
                    add_car_icon_button = Button(add_cars_frame, image=add_car_icon, compound="top", bg="#4e4f4f",
                                                 text="Add New Car", font=("arial", 16), cursor='hand2',
                                                 command=select_image, width=340, height=250)
                    add_car_icon_button.image = add_car_icon
                    add_car_icon_button.place(x=80, y=140)

                    label1 = Label(add_cars_frame, text="ADD NEW CAR", font=("Helvetica", 21, 'bold'),
                                   bg="#4e4f4f", fg='yellow')
                    label1.place(x=800, y=30, anchor="center")

                    label2 = Label(add_cars_frame, text="ENTER CAR DETAILS", font=("Helvetica", 19, 'bold'),
                                   bg="#4e4f4f", fg='white')
                    label2.place(x=1090, y=95, anchor="center")

                    car_id_label = Label(add_cars_frame, text="Car Id: ", font=("Helvetica", 19, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_id_label.place(x=630, y=165)
                    car_id_entry = Entry(add_cars_frame, width=20, fg="black", font=("yu gothic ui semibold", 12),
                                         highlightthickness=2)
                    car_id_entry.place(x=790, y=165)

                    car_name_label = Label(add_cars_frame, text="Car Name: ", font=("Helvetica", 19, 'bold'),
                                           bg="#4e4f4f", fg='white')
                    car_name_label.place(x=630, y=215)
                    car_name_entry = Entry(add_cars_frame, width=20, fg="black", font=("yu gothic ui semibold", 12),
                                           highlightthickness=2)
                    car_name_entry.place(x=790, y=215)

                    car_no_label = Label(add_cars_frame, text="Car Number", font=("Helvetica", 19, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=630, y=280)
                    car_no_entry = Entry(add_cars_frame, width=20, fg="black", font=("yu gothic ui semibold", 12),
                                         highlightthickness=2)
                    car_no_entry.place(x=790, y=280)

                    car_type_label = Label(add_cars_frame, text="Car Type", font=("Helvetica", 19, 'bold'),
                                           bg="#4e4f4f", fg='white')
                    car_type_label.place(x=630, y=340)
                    car_type_entry = Entry(add_cars_frame, width=20, fg="black", font=("yu gothic ui semibold", 12),
                                           highlightthickness=2)
                    car_type_entry.place(x=790, y=340)

                    fuel_type_label = Label(add_cars_frame, text="Fuel Type", font=("Helvetica", 19, 'bold'),
                                            bg="#4e4f4f", fg='white')
                    fuel_type_label.place(x=1030, y=155)
                    # Combobox for selecting fuel type
                    fuel_type_combobox = Combobox(add_cars_frame, values=["Petrol", "Diesel"], state="normal")
                    fuel_type_combobox.set("Select fuel ")  # Set default value to Petrol
                    fuel_type_combobox.place(x=1300, y=155)

                    transmission_type_label = Label(add_cars_frame, text="Transimission Type",
                                                    font=("Helvetica", 19, 'bold'),
                                                    bg="#4e4f4f", fg='white')
                    transmission_type_label.place(x=1030, y=215)
                    transmission_type_combobox = Combobox(add_cars_frame, values=["Automatic", "Manual"],
                                                          state="normal")
                    transmission_type_combobox.set("Select Transmission")  # Set default value to Petrol
                    transmission_type_combobox.place(x=1300, y=215)

                    ac_type_label = Label(add_cars_frame, text="AC Type", font=("Helvetica", 19, 'bold'),
                                          bg="#4e4f4f", fg='white')
                    ac_type_label.place(x=1030, y=280)
                    ac_type_combobox = Combobox(add_cars_frame, values=["NON-AC", "AC"], state="normal")
                    ac_type_combobox.set("Select AC")
                    ac_type_combobox.place(x=1300, y=280)

                    luggage_label = Label(add_cars_frame, text="Luggage Capacity", font=("Helvetica", 19, 'bold'),
                                          bg="#4e4f4f", fg='white')
                    luggage_label.place(x=1030, y=340)
                    luggage_entry = Entry(add_cars_frame, width=20, fg="black", font=("yu gothic ui semibold", 12),
                                          highlightthickness=2)
                    luggage_entry.place(x=1300, y=340)

                    seats_label = Label(add_cars_frame, text="Seats Capacity", font=("Helvetica", 19, 'bold'),
                                        bg="#4e4f4f", fg='white')
                    seats_label.place(x=1030, y=405)
                    seats_entry = Entry(add_cars_frame, width=20, fg="black", font=("yu gothic ui semibold", 12),
                                        highlightthickness=2)
                    seats_entry.place(x=1300, y=405)

                    rent_label = Label(add_cars_frame, text="Car Rent", font=("Helvetica", 19, 'bold'),
                                       bg="#4e4f4f", fg='white')
                    rent_label.place(x=630, y=405)
                    rent_entry = Entry(add_cars_frame, width=20, fg="black", font=("yu gothic ui semibold", 12),
                                       highlightthickness=2)
                    rent_entry.place(x=790, y=405)

                    def check_fields():
                        # Retrieve values from entry fields
                        car_id = car_id_entry.get()
                        car_no = car_no_entry.get()
                        car_name = car_name_entry.get()
                        seats_capacity = seats_entry.get()
                        luggage_capacity = luggage_entry.get()
                        transmission_type = transmission_type_combobox.get()
                        fuel_type = fuel_type_combobox.get()
                        car_type = car_type_entry.get()
                        ac_type = ac_type_combobox.get()
                        car_rent = rent_entry.get()

                        # Check if any entry is empty
                        if not all((car_id, car_name, car_no, car_type, fuel_type, transmission_type, ac_type,
                                    luggage_capacity, seats_capacity, car_rent)):
                            messagebox.showerror("Error", "Please fill in all fields.")
                        else:
                            # If all fields are filled, ask user if they want to add the new car
                            response = messagebox.askyesno("Confirmation", "Do you want to add the new car?")

                            # If user confirms, proceed with adding the new car
                            if response:
                                insert_car_data(car_id, car_name, car_no, car_type, fuel_type, transmission_type,
                                                luggage_capacity, seats_capacity, car_rent)

                    add_button = Button(add_cars_frame, text="ADD", fg='white', bg='#1b87d2', width=8,
                                        font=("yu gothic ui bold", 16), command=check_fields)
                    add_button.place(x=900, y=530)

                    def insert_car_data(car_id, car_number, car_name, seats_capacity, luggage_capacity,
                                        transmission_type, fuel_type, car_type, car_rent):
                        # Connect to the database
                        conn = sqlite3.connect('Car_Rental_Management_Database.db')
                        cursor = conn.cursor()

                        # Check if the car_id and car_name combination already exists
                        cursor.execute("SELECT * FROM Cars_info WHERE car_id = ? OR car_name = ?", (car_id, car_name))
                        existing_car = cursor.fetchone()

                        # If the car_id and car_name combination already exists, display a messagebox
                        if existing_car:
                            messagebox.showerror("Error", "Car already exists in the System.")
                        else:
                            # Insert the data into the Cars_info table
                            cursor.execute(
                                "INSERT INTO Cars_info (car_id, car_number, car_name, seats_capacity, luggage_capacity,"
                                "transmission_type, fuel_type, car_type, vehicle_rent) VALUES (?, ?, ?, ?, ?, ?, ?, "
                                "?, ?)",
                                (car_id, car_name, car_number, car_type, fuel_type, transmission_type,
                                 luggage_capacity, seats_capacity, car_rent))
                            conn.commit()
                            cursor.close()
                            conn.close()

                        def update_new_car_values_in_file(file_name):  # function to update the value of new_car@X to 1
                            # Read data from file
                            with open(file_name, "r") as file:
                                data = file.readlines()

                            # Create dictionaries to store old car and new car information
                            old_cars = {}
                            new_cars = {}

                            # Extract old car and new car information from data
                            for line in data:
                                # Check if the line contains the expected separator (": ")
                                if ": " in line:
                                    parts = line.strip().split(": ", 1)  # Split only once
                                    if len(parts) == 2:
                                        key, value = parts
                                        if key.startswith("old_car@"):
                                            old_cars[key] = int(value)
                                        elif key.startswith("new_car@"):
                                            new_cars[key] = int(value)

                            # Update new car values based on old car values
                            for i in range(1, 17):
                                old_key = f"old_car@{i}"
                                new_key = f"new_car@{i}"
                                if old_cars.get(old_key, -1) == 1:
                                    new_cars[new_key] = 1

                            # Update data in memory
                            for key, value in new_cars.items():
                                for i, line in enumerate(data):
                                    if line.startswith(key):
                                        data[i] = f"{key}: {value}\n"
                                        break

                            # Write updated data back to file
                            with open(file_name, "w") as file:
                                file.writelines(data)
                            print("New car values updated successfully!")

                        def update_car_path():  # function to add the path of the new car image
                            global new_image_path
                            # Open the file and read all lines
                            with open('car_data.txt', 'r') as file:
                                lines = file.readlines()

                            car_number = None
                            for line in lines:
                                key, value = line.strip().split(': ')
                                if key.startswith('car') and value == '0' or value == '':
                                    car_number = int(key[-1])  # Extract last digit of the key
                                    break
                                print("NEW CAR NUMBER = ", car_number)

                            # If car number is found, update the corresponding new_car_pathX
                            if car_number is not None:
                                new_car_path_key = f"new_car_path{car_number}"
                                print("NEW PATH KEY = ", new_car_path_key)
                                # Iterate over the lines to find and update the corresponding new_car_pathX line
                                for i, line in enumerate(lines):
                                    if line.startswith(new_car_path_key):
                                        lines[i] = f"{new_car_path_key}: {new_image_path}\n"
                                        break  # Exit the loop after updating the first occurrence

                            # Write the updated lines back to the file
                            with open('car_data.txt', 'w') as file:
                                file.writelines(lines)

                        def update_vehicle_values(vehicle_name):  # function to update the carX with new car name
                            # Read the contents of the file
                            with open("car_data.txt", "r") as file:
                                lines = file.readlines()

                            # Iterate through the lines and update any zero car values
                            for i, line in enumerate(lines):
                                if line.startswith("car"):
                                    key, value = line.strip().split(":")
                                    car_number = key.strip()[3:]  # Extract the car number from the key
                                    if value.strip() == "0":
                                        lines[i] = f"{key.strip()}: {vehicle_name}\n"
                                        break
                            print("UPDATED THE CAR DATA IN THE FILE\n")

                            # Write the updated content back to the file
                            with open("car_data.txt", "w") as file:
                                file.writelines(lines)

                        def read_car_data(file_name):
                            # Open the file and read all lines
                            with open(file_name, 'r') as file:
                                lines = file.readlines()

                            # Print the content of the file
                            for line in lines:
                                print(line.strip())  # Strip removes leading/trailing whitespaces and newlines

                        def update_car_value_2(file_name, new_image_path, car_variable):
                            # Read data from file
                            with open(file_name, "r") as file:
                                lines = file.readlines()

                            # Iterate through lines to find the first car key with value 0
                            for line in lines:
                                if ": 0\n" in line:
                                    # Extract car key and update its value
                                    car_key = line.split(":")[0]
                                    new_car_key = f"new_car@{car_key[3:]}"
                                    new_car_path_key = f"new_car_path{car_key[3:]}"

                                    # Update new_car@X value to 1 and new_car_pathX to new_image_path
                                    for j, line in enumerate(lines):
                                        if line.startswith(new_car_key):
                                            lines[j] = f"{new_car_key}: 1\n"
                                        elif line.startswith(new_car_path_key):
                                            lines[j] = f"{new_car_path_key}: {new_image_path}\n"
                                        elif line.startswith(car_key):
                                            lines[j] = f"{car_key}: {car_variable}\n"

                                    # Write updated lines back to the file
                                    with open(file_name, "w") as file:
                                        file.writelines(lines)
                                    break  # Stop processing after updating the first occurrence

                        def count_zeros(file_name):
                            zero_count_line1_to_9 = 0
                            zero_count_line10_to_16 = 0
                            has_zero_value_line1_to_9 = False

                            # Read data from file
                            with open(file_name, "r") as file:
                                lines = file.readlines()

                            # Check for keys from 'car1' to 'car9'
                            for i in range(1, 10):
                                car_key = f"car{i}: 0\n"
                                if car_key in lines:
                                    zero_count_line1_to_9 += 1
                                    has_zero_value_line1_to_9 = True

                            # If no zeroes are found from 'car1' to 'car9', then check for keys from 'car10' to 'car16'
                            if not has_zero_value_line1_to_9:
                                for i in range(10, 17):
                                    car_key = f"car{i}: 0\n"
                                    if car_key in lines:
                                        zero_count_line10_to_16 += 1

                            return zero_count_line1_to_9, zero_count_line10_to_16

                        zero_count_line1_to_9, zero_count_line10_to_16 = count_zeros("car_data.txt")
                        print("The value of 1st 0s and 2nd zeros are = ", zero_count_line1_to_9, zero_count_line10_to_16)

                        if zero_count_line10_to_16 >= 1 and zero_count_line1_to_9 == False:
                            global new_image_path
                            print(new_image_path)
                            update_car_value_2("car_data2.txt", new_image_path, car_number)

                        else:
                            update_new_car_values_in_file("car_data.txt")
                            update_car_path()
                            update_vehicle_values(
                                car_number)  # Pass car_number(car_name) obtained from insert operation
                            read_car_data('car_data.txt')

                        messagebox.showinfo("Success", "The New car has been successfully Added in the system.")

                add_car_image = PhotoImage(file="images/new_car.png")
                add_car_button = Button(admin_main_dashframe, image=add_car_image, compound="top", bg="pink",
                                        text="Add New Car", font=("arial", 16), cursor='hand2', command=add_cars)
                add_car_button.image = add_car_image
                add_car_button.place(x=0, y=150, width=220, height=158)

                def remove_cars():  # function to remove a specific car from the system
                    def search_car():
                        global button_pressed_before
                        # Get the car ID entered by the user
                        car_id = car_id_entry.get()

                        # Connect to the database
                        conn = sqlite3.connect('Car_Rental_Management_Database.db')
                        cursor = conn.cursor()

                        # Execute the query to find the car
                        cursor.execute("SELECT * FROM Cars_info WHERE car_id = ?", (car_id,))
                        car_data = cursor.fetchone()

                        if car_data:
                            if button_pressed_before:
                                print("hello")
                                car_name_label1 = Label(remove_cars_frame, text=car_data[2],
                                                        font=("Helvetica", 19, 'bold'),
                                                        bg="#4e4f4f", fg='#f5d03d')
                                car_name_label1.place(x=440, y=155)

                                car_no_label1 = Label(remove_cars_frame, text=car_data[1],
                                                      font=("Helvetica", 19, 'bold'),
                                                      bg="#4e4f4f", fg='#f5d03d')
                                car_no_label1.place(x=440, y=215)

                                car_type_label1 = Label(remove_cars_frame, text=car_data[7],
                                                        font=("Helvetica", 19, 'bold'),
                                                        bg="#4e4f4f", fg='#f5d03d')
                                car_type_label1.place(x=440, y=280)

                                fuel_type_label1 = Label(remove_cars_frame, text=car_data[6],
                                                         font=("Helvetica", 19, 'bold'),
                                                         bg="#4e4f4f", fg='#f5d03d')
                                fuel_type_label1.place(x=1180, y=155)

                                transmission_type_label1 = Label(remove_cars_frame, text=car_data[5],
                                                                 font=("Helvetica", 19, 'bold'),
                                                                 bg="#4e4f4f", fg='#f5d03d')
                                transmission_type_label1.place(x=1180, y=215)

                                ac_type_label1 = Label(remove_cars_frame, text="AC", font=("Helvetica", 19, 'bold'),
                                                       bg="#4e4f4f", fg='#f5d03d')
                                ac_type_label1.place(x=1180, y=280)

                                luggage_label1 = Label(remove_cars_frame, text=car_data[4],
                                                       font=("Helvetica", 19, 'bold'),
                                                       bg="#4e4f4f", fg='#f5d03d')
                                luggage_label1.place(x=440, y=405)

                                seats_label1 = Label(remove_cars_frame, text=car_data[3],
                                                     font=("Helvetica", 19, 'bold'),
                                                     bg="#4e4f4f", fg='#f5d03d')
                                seats_label1.place(x=1180, y=340)

                                rent_label1 = Label(remove_cars_frame, text=car_data[8], font=("Helvetica", 19, 'bold'),
                                                    bg="#4e4f4f", fg='#f5d03d')
                                rent_label1.place(x=440, y=340)

                                # Destroy only specified labels
                                '''car_name_label1.destroy()
                                car_no_label1.destroy()
                                car_type_label1.destroy()
                                fuel_type_label1.destroy()
                                transmission_type_label1.destroy()
                                ac_type_label1.destroy()
                                luggage_label1.destroy()
                                seats_label1.destroy()
                                rent_label1.destroy()'''

                            else:
                                print("hi")
                                car_name_label1 = Label(remove_cars_frame, text=car_data[2],
                                                        font=("Helvetica", 19, 'bold'),
                                                        bg="#4e4f4f", fg='#f5d03d')
                                car_name_label1.place(x=440, y=155)

                                car_no_label1 = Label(remove_cars_frame, text=car_data[1],
                                                      font=("Helvetica", 19, 'bold'),
                                                      bg="#4e4f4f", fg='#f5d03d')
                                car_no_label1.place(x=440, y=215)

                                car_type_label1 = Label(remove_cars_frame, text=car_data[7],
                                                        font=("Helvetica", 19, 'bold'),
                                                        bg="#4e4f4f", fg='#f5d03d')
                                car_type_label1.place(x=440, y=280)

                                fuel_type_label1 = Label(remove_cars_frame, text=car_data[6],
                                                         font=("Helvetica", 19, 'bold'),
                                                         bg="#4e4f4f", fg='#f5d03d')
                                fuel_type_label1.place(x=1180, y=155)

                                transmission_type_label1 = Label(remove_cars_frame, text=car_data[5],
                                                                 font=("Helvetica", 19, 'bold'),
                                                                 bg="#4e4f4f", fg='#f5d03d')
                                transmission_type_label1.place(x=1180, y=215)

                                ac_type_label1 = Label(remove_cars_frame, text="AC", font=("Helvetica", 19, 'bold'),
                                                       bg="#4e4f4f", fg='#f5d03d')
                                ac_type_label1.place(x=1180, y=280)

                                luggage_label1 = Label(remove_cars_frame, text=car_data[4],
                                                       font=("Helvetica", 19, 'bold'),
                                                       bg="#4e4f4f", fg='#f5d03d')
                                luggage_label1.place(x=440, y=405)

                                seats_label1 = Label(remove_cars_frame, text=car_data[3],
                                                     font=("Helvetica", 19, 'bold'),
                                                     bg="#4e4f4f", fg='#f5d03d')
                                seats_label1.place(x=1180, y=340)

                                rent_label1 = Label(remove_cars_frame, text=car_data[8], font=("Helvetica", 19, 'bold'),
                                                    bg="#4e4f4f", fg='#f5d03d')
                                rent_label1.place(x=440, y=340)

                                button_pressed_before = True

                                # Car found, display the data
                                print("Car Found!")
                                print("Car Data:", car_data)

                        else:
                            # Car not found
                            messagebox.showinfo("Car Not Found", "The car with ID {} was not found in the database."
                                                                 " Please verify the car ID and try again.".format(
                                car_id))

                        # Close the connection
                        conn.close()

                    def confirm_removal(car_id):
                        # Display a message box with Yes and No options
                        result = messagebox.askyesno("Confirmation",
                                                     "Are you sure you want to remove this car from the system?")
                        # Check the user's response
                        if result:
                            delete_car_data(car_id)
                            print("Car removed from the system")
                        else:
                            print("Removal cancelled")

                    def delete_car_data(c_id):
                        def update_car_data(car_name):  # function to update the carX to 0 and old_car_X to 1
                            try:
                                # Read data from the file
                                with open("car_data.txt", "r") as file:
                                    lines = file.readlines()

                                # Update car data and old car data
                                for i, line in enumerate(lines):
                                    if line.startswith("car"):
                                        key, value = line.strip().split(": ")
                                        if value == car_name:
                                            car_number = key[-1]  # Obtain the last digit of the key
                                            print(car_number)
                                            old_car_key = f"old_car@{car_number}"
                                            print(old_car_key)
                                            # Update carX value to "0"
                                            lines[i] = f"{key}: 0\n"
                                            # Update old_car@X value to "1"
                                            for j, inner_line in enumerate(lines):
                                                if old_car_key in inner_line:
                                                    lines[j] = f"{old_car_key}: 1\n"
                                                    print(lines[j])
                                                    print("THe old car is changed to 1")
                                                    break

                                # Write updated data back to the file
                                with open("car_data.txt", "w") as file:
                                    file.writelines(lines)

                            except FileNotFoundError:
                                print("Car data file not found.")

                        # Connect to the database
                        conn1 = sqlite3.connect('Car_Rental_Management_Database.db')
                        cursor1 = conn1.cursor()

                        cursor1.execute("SELECT car_name FROM Cars_info WHERE car_id = ?", (c_id,))
                        car_name = cursor1.fetchone()[0]  # Fetch the first result
                        print(car_name)

                        update_car_data(car_name)  # car_name is the name of the car which is being passed

                        # Execute the DELETE query
                        cursor1.execute("DELETE FROM Cars_info WHERE car_id = ?", (c_id,))

                        # Commit the transaction
                        conn1.commit()

                        # Close the cursor and connection
                        cursor1.close()
                        conn1.close()

                        # Display success message
                        messagebox.showinfo("Success", "The car has been successfully removed from the system.")

                    remove_cars_frame = Frame(admin_main_dashframe, width=1600, height=700, background="#4e4f4f")
                    remove_cars_frame.place(x=0, y=310)

                    label1 = Label(remove_cars_frame, text="REMOVE EXISTING CAR", font=("Helvetica", 21, 'bold'),
                                   bg="#4e4f4f", fg='yellow')
                    label1.place(x=800, y=30, anchor="center")

                    car_id_label = Label(remove_cars_frame, text="Enter Car Id ", font=("Helvetica", 19, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_id_label.place(x=670, y=80)
                    car_id_entry = Entry(remove_cars_frame, width=7, fg="black", font=("yu gothic ui semibold", 12),
                                         highlightthickness=2)
                    car_id_entry.place(x=850, y=84)

                    car_name_label = Label(remove_cars_frame, text="Car Name: ", font=("Helvetica", 19, 'bold'),
                                           bg="#4e4f4f", fg='white')
                    car_name_label.place(x=135, y=155)

                    car_no_label = Label(remove_cars_frame, text="Car Number: ", font=("Helvetica", 19, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=135, y=215)

                    car_type_label = Label(remove_cars_frame, text="Car Type:", font=("Helvetica", 19, 'bold'),
                                           bg="#4e4f4f", fg='white')
                    car_type_label.place(x=135, y=280)

                    fuel_type_label = Label(remove_cars_frame, text="Fuel Type:", font=("Helvetica", 19, 'bold'),
                                            bg="#4e4f4f", fg='white')
                    fuel_type_label.place(x=840, y=155)
                    transmission_type_label = Label(remove_cars_frame, text="Transimission Type:",
                                                    font=("Helvetica", 19, 'bold'),
                                                    bg="#4e4f4f", fg='white')
                    transmission_type_label.place(x=840, y=215)

                    ac_type_label = Label(remove_cars_frame, text="AC Type:", font=("Helvetica", 19, 'bold'),
                                          bg="#4e4f4f", fg='white')
                    ac_type_label.place(x=840, y=280)

                    luggage_label = Label(remove_cars_frame, text="Luggage Capacity:", font=("Helvetica", 19, 'bold'),
                                          bg="#4e4f4f", fg='white')
                    luggage_label.place(x=135, y=405)

                    seats_label = Label(remove_cars_frame, text="Seats Capacity:", font=("Helvetica", 19, 'bold'),
                                        bg="#4e4f4f", fg='white')
                    seats_label.place(x=840, y=340)

                    rent_label = Label(remove_cars_frame, text="Car Rent:", font=("Helvetica", 19, 'bold'),
                                       bg="#4e4f4f", fg='white')
                    rent_label.place(x=135, y=340)

                    remove_button = Button(remove_cars_frame, text="Remove Car", fg='white', bg='#1b87d2', width=13,
                                           font=("yu gothic ui bold", 16),
                                           command=lambda: confirm_removal(car_id_entry.get()))
                    remove_button.place(x=510, y=570)

                    search_car_button = Button(remove_cars_frame, text="Search", fg='white', bg='#1b87d2', width=6,
                                               font=("yu gothic ui bold", 16), command=search_car)
                    search_car_button.place(x=1000, y=71)

                    removal_reason_label = Label(remove_cars_frame, text="Reason for Removal: ",
                                                 font=("Helvetica", 19, 'bold'), bg="#4e4f4f", fg='white')
                    removal_reason_label.place(x=840, y=410)
                    removal_reason = Text(remove_cars_frame, bg='white', width=50, height=6, highlightthickness=0,
                                          borderwidth=0, font="Helvetica")
                    removal_reason.place(x=940, y=470)

                    '''image2 = PhotoImage(file="images/scorpio1.png")
                    image_label2 = Label(remove_cars_frame, image=image2, background='#e4edf0', bd=0)

                    image_label2 = Label(remove_cars_frame, image=image2, background='#e4edf0', bd=3, relief="solid")
                    image_label2.image = image2

                    image_label2.place(x=80, y=140, width=450, height=320)'''

                remove_car_image = PhotoImage(file="images/remove_cars.png")
                remove_car_button = Button(admin_main_dashframe, image=remove_car_image, compound="top", bg="pink",
                                           text="Remove Car", font=("arial", 16), cursor='hand2', command=remove_cars)
                remove_car_button.image = remove_car_image
                remove_car_button.place(x=221, y=150, width=220, height=158)

                def display_rented_cars(rented_cars_frame):
                    connection = sqlite3.connect("Car_Rental_Management_Database.db")
                    cur = connection.cursor()
                    cur.execute("SELECT * FROM Rented_cars")
                    all_cars_list = cur.fetchall()

                    cars = []
                    for a, b, c, d, e, f, g in all_cars_list:  # displays the list of all rented cars
                        cars.append([a, b, c, d, e, f, g])

                    label_characteristics = {
                        "font": ("Helvetica", 12),
                        "bg": "#4e4f4f",
                        "fg": "white"
                    }

                    # Create labels dynamically for each car
                    for i, car_info in enumerate(all_cars_list):
                        labels_info = [
                            {"text": car_info[0], "x": 100},
                            {"text": car_info[1], "x": 240},
                            {"text": car_info[2], "x": 418},
                            {"text": car_info[3], "x": 643},
                            {"text": car_info[4], "x": 868},
                            {"text": car_info[5], "x": 1100},
                            {"text": car_info[6], "x": 1320},
                        ]

                        # Create labels dynamically for each characteristic
                        for j, label_info in enumerate(labels_info):
                            label = Label(rented_cars_frame, text=label_info["text"], **label_characteristics)
                            label.place(x=label_info["x"], y=115 + i * 43)

                def rented_cars():  # function to see all the rented cars
                    # Connect to the database
                    conn = sqlite3.connect('Car_Rental_Management_Database.db')
                    cursor = conn.cursor()
                    # Execute the query to get the total number of rows
                    cursor.execute("SELECT COUNT(*) FROM Rented_cars")
                    total_rows = cursor.fetchone()[0]

                    cursor.close()
                    conn.close()

                    rented_cars_frame = Frame(admin_main_dashframe, width=1600, height=700, background="yellow")
                    rented_cars_frame.place(x=0, y=310)

                    canvas = Canvas(rented_cars_frame, width=1600, height=650, background="#4e4f4f")
                    canvas.pack()

                    canvas.create_line(70, 50, 1470, 50, width=2, fill="black")
                    canvas.create_line(70, 95, 1470, 95, width=2, fill="black")
                    canvas.create_line(70, 50, 70, 605, width=2, fill="black")
                    canvas.create_line(190, 50, 190, 605, width=2, fill="black")
                    canvas.create_line(395, 50, 395, 605, width=2, fill="black")
                    canvas.create_line(595, 50, 595, 605, width=2, fill="black")
                    canvas.create_line(815, 50, 815, 605, width=2, fill="black")
                    canvas.create_line(1050, 50, 1050, 605, width=2, fill="black")
                    canvas.create_line(1250, 50, 1250, 605, width=2, fill="black")
                    canvas.create_line(1470, 50, 1470, 605, width=2, fill="black")

                    label1 = Label(canvas, text="RENTED CAR LIST", font=("Helvetica", 22, 'bold'),
                                   bg="#4e4f4f", fg='yellow')
                    label1.place(relx=0.5, rely=0.03, anchor="center")

                    car_id_label = Label(rented_cars_frame, text="Car Id", font=("Helvetica", 15, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_id_label.place(x=100, y=60)

                    car_name_label = Label(rented_cars_frame, text="Car Number", font=("Helvetica", 15, 'bold'),
                                           bg="#4e4f4f", fg='white')
                    car_name_label.place(x=240, y=60)

                    car_no_label = Label(rented_cars_frame, text="Car Name", font=("Helvetica", 15, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=430, y=60)

                    seats_label = Label(rented_cars_frame, text="Customer Name", font=("Helvetica", 15, 'bold'),
                                        bg="#4e4f4f", fg='white')
                    seats_label.place(x=620, y=60)

                    luggage_label = Label(rented_cars_frame, text="Customer Contact No.", font=("Helvetica", 15,
                                                                                                'bold'), bg="#4e4f4f",
                                          fg='white')
                    luggage_label.place(x=820, y=60)

                    type_label = Label(rented_cars_frame, text="Pick-UP Date", font=("Helvetica", 15, 'bold'),
                                       bg="#4e4f4f", fg='white')
                    type_label.place(x=1080, y=60)

                    type_label = Label(rented_cars_frame, text="Drop-Off Date", font=("Helvetica", 15, 'bold'),
                                       bg="#4e4f4f", fg='white')
                    type_label.place(x=1190 + 100, y=60)

                    total_rented = Label(rented_cars_frame, text="TOTAL RENTED CARS:   " + str(total_rows),
                                         font=("Helvetica", 16, "bold"), bg="#4e4f4f", fg='yellow')
                    total_rented.place(x=400, y=615)

                    canvas.create_line(70, 145, 1470, 145, width=2, fill="black")
                    canvas.create_line(70, 195, 1470, 195, width=2, fill="black")
                    canvas.create_line(70, 250, 1470, 250, width=2, fill="black")
                    canvas.create_line(70, 305, 1470, 305, width=2, fill="black")
                    canvas.create_line(70, 355, 1470, 355, width=2, fill="black")
                    canvas.create_line(70, 405, 1470, 405, width=2, fill="black")
                    canvas.create_line(70, 455, 1470, 455, width=2, fill="black")
                    canvas.create_line(70, 505, 1470, 505, width=2, fill="black")
                    canvas.create_line(70, 555, 1470, 555, width=2, fill="black")
                    canvas.create_line(70, 605, 1470, 605, width=2, fill="black")

                    display_rented_cars(rented_cars_frame)

                rented_car_image = PhotoImage(file="images/rented_cars.png")
                rented_car_button = Button(admin_main_dashframe, image=rented_car_image, compound="top", bg="pink",
                                           text="Rented Cars", font=("arial", 16), cursor='hand2', command=rented_cars)
                rented_car_button.image = rented_car_image
                rented_car_button.place(x=442, y=150, width=220, height=158)

                def cars_history():  # function to search the specific car history
                    def car_history_search(vehicle_id):
                        con = sqlite3.connect("Car_Rental_Management_Database.db")
                        cursor = con.cursor()
                        cursor.execute("SELECT * FROM Car_history WHERE Car_id = ?", (vehicle_id,))
                        selected_car_history = cursor.fetchall()
                        car_history_details1 = selected_car_history
                        print(car_history_details)

                        if selected_car_history:
                            display_car_history(car_history_details1)
                        else:
                            messagebox.showinfo("Car Rental Status", "THE CAR HAS NOT BEEN RENTED YET")

                    def display_car_history(history_info):
                        dynamic_labels = []

                        def clear_labels():
                            for label in dynamic_labels:
                                label.destroy()

                            dynamic_labels.clear()
                            total_rented.destroy()
                            total_revenue.destroy()

                        label_characteristics = {
                            "font": ("Helvetica", 12),
                            "bg": "#4e4f4f",
                            "fg": "white"
                        }

                        cars = []
                        for a, b, c, d, e, f in history_info:  # displays the list of all rented cars
                            cars.append([a, b, c, d, e, f])

                        # Create labels dynamically for each car
                        for i, car_info in enumerate(history_info):
                            labels_info = [
                                {"text": car_info[0], "x": 115},
                                {"text": car_info[1], "x": 240},
                                {"text": car_info[2], "x": 480},
                                {"text": car_info[3], "x": 773},
                                {"text": car_info[4], "x": 1010},
                                {"text": "Rs  " + str(car_info[5]), "x": 1238}
                            ]

                            # Create labels dynamically for each characteristic
                            for j, label_info in enumerate(labels_info):
                                label2 = Label(cars_history_frame, text=label_info["text"], **label_characteristics)
                                label2.place(x=label_info["x"], y=145 + i * 46)
                                dynamic_labels.append(label2)

                        clear_button = Button(cars_history_frame, text="Clear", fg='white', bg='#1b87d2', width=6,
                                              font=("yu gothic ui bold", 16), command=clear_labels)
                        clear_button.place(x=1390, y=593)

                        total_sum = 0
                        for row in history_info:
                            total_sum += row[5]

                        total_rented = Label(cars_history_frame, text=str(len(history_info)), font=("Helvetica", 16,
                                                                                                    "bold"),
                                             bg="#4e4f4f", fg='yellow')
                        total_rented.place(x=565, y=600)

                        total_revenue = Label(cars_history_frame, text=str(total_sum), font=("Helvetica", 16, "bold"),
                                              bg="#4e4f4f", fg='yellow')
                        total_revenue.place(x=1120, y=600)

                    cars_history_frame = Frame(admin_main_dashframe, width=1600, height=700, background="#4e4f4f")
                    cars_history_frame.place(x=0, y=310)

                    canvas = Canvas(cars_history_frame, width=1600, height=650, background="#4e4f4f")
                    canvas.pack()

                    canvas.create_line(90, 80, 1440, 80, width=2, fill="black")
                    canvas.create_line(90, 80, 90, 582, width=2, fill="black")
                    canvas.create_line(200, 80, 200, 582, width=2, fill="black")
                    canvas.create_line(410, 80, 410, 582, width=2, fill="black")
                    canvas.create_line(700, 80, 700, 582, width=2, fill="black")
                    canvas.create_line(950, 80, 950, 582, width=2, fill="black")
                    canvas.create_line(1180, 80, 1180, 582, width=2, fill="black")
                    canvas.create_line(1440, 80, 1440, 582, width=2, fill="black")
                    canvas.create_line(90, 480, 1440, 480, width=2, fill="black")
                    canvas.create_line(90, 530, 1440, 530, width=2, fill="black")
                    canvas.create_line(90, 580, 1440, 580, width=2, fill="black")

                    label1 = Label(canvas, text="CAR HISTORY", font=("Helvetica", 21, 'bold'),
                                   bg="#4e4f4f", fg='yellow')
                    label1.place(relx=0.5, rely=0.04, anchor="center")

                    car_id_label = Label(cars_history_frame, text="Enter Car Id ", font=("Helvetica", 19, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_id_label.place(relx=0.74, rely=0.07, anchor="center")
                    car_id_entry = Entry(cars_history_frame, width=7, fg="black", font=("yu gothic ui semibold", 12),
                                         highlightthickness=2)
                    car_id_entry.place(x=1275, y=30)

                    car_id_label1 = Label(cars_history_frame, text="Car Id", font=("Helvetica", 15, 'bold'),
                                          bg="#4e4f4f", fg='white')
                    car_id_label1.place(x=110, y=90)
                    canvas.create_line(90, 130, 1440, 130, width=2, fill="black")

                    car_name_label = Label(canvas, text="Car Name", font=("Helvetica", 15, 'bold'),
                                           bg="#4e4f4f", fg='white')
                    car_name_label.place(x=270, y=90)
                    canvas.create_line(90, 180, 1440, 180, width=2, fill="black")
                    canvas.create_line(90, 230, 1440, 230, width=2, fill="black")

                    seats_label = Label(cars_history_frame, text='Customer Name', font=("Helvetica", 15, 'bold'),
                                        bg="#4e4f4f", fg='white')
                    seats_label.place(x=470, y=90)
                    canvas.create_line(90, 280, 1440, 280, width=2, fill="black")
                    canvas.create_line(90, 330, 1440, 330, width=2, fill="black")

                    type_label = Label(cars_history_frame, text="Pick-UP Date", font=("Helvetica", 15, 'bold'),
                                       bg="#4e4f4f", fg='white')
                    type_label.place(x=770, y=90)
                    canvas.create_line(90, 380, 1440, 380, width=2, fill="black")

                    type_label = Label(cars_history_frame, text="Drop-Off Date", font=("Helvetica", 15, 'bold'),
                                       bg="#4e4f4f", fg='white')
                    type_label.place(x=1000, y=90)
                    canvas.create_line(90, 430, 1440, 430, width=2, fill="black")

                    type_label = Label(cars_history_frame, text="Revenue Generated", font=("Helvetica", 15, 'bold'),
                                       bg="#4e4f4f", fg='white')
                    type_label.place(x=1210, y=90)

                    total_rented_label = Label(cars_history_frame, text="TOTAL BOOKINGS:", font=("Helvetica", 16,
                                                                                                 "bold"), bg="#4e4f4f",
                                               fg='yellow')
                    total_rented_label.place(x=360, y=600)

                    total_revenue_label = Label(cars_history_frame, text="TOTAL REVENUE GENERATED:  Rs ",
                                                font=("Helvetica", 16, "bold"), bg="#4e4f4f", fg='yellow')
                    total_revenue_label.place(x=760, y=600)

                    search_car_button = Button(cars_history_frame, text="Search", fg='white', bg='#1b87d2', width=6,
                                               font=("yu gothic ui bold", 16),
                                               command=lambda: car_history_search(car_id_entry.get()))
                    search_car_button.place(x=1390, y=15)

                car_history_image = PhotoImage(file="images/cars_history.png")
                car_history_button = Button(admin_main_dashframe, image=car_history_image, compound="top", bg="pink",
                                            text="Car History", font=("arial", 16), cursor='hand2',
                                            command=cars_history)
                car_history_button.image = car_history_image
                car_history_button.place(x=662, y=150, width=220, height=158)

                def recieve_back_cars():  # function to recieve back car from the user
                    recieve_cars_frame = Frame(admin_main_dashframe, width=1600, height=700, background="#4e4f4f")
                    recieve_cars_frame.place(x=0, y=310)
                    global total_fine

                    import sqlite3
                    from time import sleep

                    def display_transaction_details(car_rent, fine):
                        new_frame = Frame(recieve_cars_frame, width=510, height=390, bg='white', highlightthickness=1,
                                          borderwidth=1, highlightcolor='Black', highlightbackground='black')
                        new_frame.place(x=550, y=100)

                        design_frame = Listbox(new_frame, bg='#9211cf', width=100, height=7, highlightthickness=0,
                                               borderwidth=0)
                        design_frame.place(x=0, y=0)

                        payment_label = Label(new_frame, text="Payment Details", font=("yu gothic ui bold", 23),
                                              bg='#9211cf', fg='Black')
                        payment_label.place(x=160, y=17)

                        rent_label = Label(new_frame, text="Rent Amount", font=("yu gothic ui bold", 17),
                                           bg='white', fg='black')
                        rent_label.place(x=30, y=140)

                        rent_amount = Label(new_frame, text="Rs " + str(car_rent), font=("yu gothic ui bold", 17),
                                            bg='white', fg='#4f4e4e')
                        rent_amount.place(x=48, y=180)

                        fine_label = Label(new_frame, text="Fine Amount", font=("yu gothic ui bold", 17),
                                           bg='white', fg='black')
                        fine_label.place(x=200, y=140)

                        fine_amount = Label(new_frame, text="Rs " + str(fine), font=("yu gothic ui bold", 17),
                                            bg='white', fg='#4f4e4e')
                        fine_amount.place(x=220, y=180)

                        total_label = Label(new_frame, text="Total Amount", font=("yu gothic ui bold", 17),
                                            bg='white', fg='black')
                        total_label.place(x=355, y=140)

                        total1 = Label(new_frame, text="Rs " + str(car_rent + fine), font=("yu gothic ui bold", 17),
                                       bg='white', fg='#4f4e4e')
                        total1.place(x=369, y=180)

                        continue_button = Button(new_frame, text="Continue", fg='white', bg='#1b87d2',
                                                 width=10, font=("yu gothic ui bold", 15), command=lambda:
                            (new_frame.destroy(), display_successfull_message()))
                        continue_button.place(x=180, y=310)

                    total_fine = 0

                    def display_successfull_message():

                        # Create a new frame for the selected option
                        new_frame = Frame(recieve_cars_frame, width=500, height=500, bg='white', highlightthickness=3,
                                          borderwidth=3, highlightcolor='Black', highlightbackground='black')
                        new_frame.place(x=550, y=100)  # Adjust the position as needed

                        image_path = "images/check.png"
                        image = PhotoImage(file=image_path)

                        # Create a Label to display the image
                        image_label = Label(new_frame, image=image, bg="white")
                        image_label.image = image  # Keep a reference to the image object
                        image_label.place(relx=0.5, rely=0.2, anchor="center")

                        label2 = Label(new_frame, text='Car Received Successfully', bg='white', fg='black', font=
                        ("yu gothic ui bold", 20, 'bold'))
                        label2.place(x=105, y=270)

                        continue_button = Button(new_frame, text="Continue", fg='white', bg='#1b87d2',
                                                 width=10, font=("yu gothic ui bold", 15), command=new_frame.destroy)
                        continue_button.place(x=180, y=410)

                    def take_car_back(car_id):
                        global total_fine

                        con = sqlite3.connect("Car_Rental_Management_Database.db")
                        cursor = con.cursor()
                        cursor.execute("SELECT * FROM Rented_car_list WHERE Car_id = ?", (car_id,))
                        car_details = cursor.fetchall()
                        print("Details of the car fetched from Rented_car_list = ", car_details)
                        cursor.close()

                        conn = sqlite3.connect("Car_Rental_Management_Database.db")
                        conn.execute('''INSERT INTO Cars_info(Car_id, Car_number, Car_name, Seats_capacity, 
                                        luggage_capacity, transmission_type, fuel_type,car_type, vehicle_rent ) 
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                     (car_details[0][0], car_details[0][1], car_details[0][2], car_details[0][3],
                                      car_details[0][4], car_details[0][5], car_details[0][6], car_details[0][7],
                                      car_details[0][8]))
                        conn.commit()
                        conn.close()

                        sleep(0.2)  # Sleep after committing the transaction

                        cursor = con.cursor()  # Reuse the existing connection
                        query1 = """
                                SELECT Revenue_generated, Customer_name
                                FROM Car_history
                                WHERE car_id = ? 
                                  AND Departure_Date = ?;
                                """
                        cursor.execute(query1, (car_details[0][0], departure_date))
                        result = cursor.fetchone()
                        print("RESULT = ", result)
                        print("Departure date when query is being run", departure_date)

                        query = """
                                UPDATE Car_history
                                SET Revenue_generated = ?
                                WHERE car_id = ? 
                                  AND customer_name = ? 
                                  AND Departure_Date = ?;
                                """
                        cursor.execute(query, (result[0] + total_fine, car_details[0][0], result[1], departure_date))
                        con.commit()

                        cursor.execute("DELETE FROM Rented_car_list WHERE Car_id = ?", (car_id,))
                        cursor.execute("DELETE FROM Rented_cars WHERE Car_id = ?", (car_id,))
                        con.commit()

                        con.close()  # Close the connection at the end

                        display_transaction_details(result[0], total_fine)

                    def display_car_info(car_info):
                        global departure_date
                        car_name_label1 = Label(recieve_cars_frame, text=car_info[0][2], font=("Helvetica", 17),
                                                bg="#4e4f4f", fg='#f5d03d')
                        car_name_label1.place(x=12, y=165)

                        car_no_label1 = Label(recieve_cars_frame, text=car_info[0][1], font=("Helvetica", 17),
                                              bg="#4e4f4f", fg='#f5d03d')
                        car_no_label1.place(x=268, y=165)

                        car_no_label1 = Label(recieve_cars_frame, text=car_info[0][3], font=("Helvetica", 17),
                                              bg="#4e4f4f", fg='#f5d03d')
                        car_no_label1.place(x=495, y=165)

                        car_no_label1 = Label(recieve_cars_frame, text=car_info[0][4], font=("Helvetica", 17),
                                              bg="#4e4f4f", fg='#f5d03d')
                        car_no_label1.place(x=786, y=165)
                        car_no_label1 = Label(recieve_cars_frame, text=car_info[0][5], font=("Helvetica", 17),
                                              bg="#4e4f4f", fg='#f5d03d')
                        car_no_label1.place(x=1060, y=165)

                        car_no_label1 = Label(recieve_cars_frame, text=car_info[0][6], font=("Helvetica", 17),
                                              bg="#4e4f4f", fg='#f5d03d')
                        car_no_label1.place(x=1290, y=165)

                        departure_date = car_info[0][5]
                        print("Departure Date at when details is displayed = ", departure_date)

                    def display_recive_car_info(vehicle_id):
                        con = sqlite3.connect("Car_Rental_Management_Database.db")
                        cursor = con.cursor()
                        cursor.execute("SELECT * FROM Rented_cars WHERE Car_id = ?", (vehicle_id,))
                        selected_car_history = cursor.fetchall()
                        car_details = selected_car_history
                        print(car_history_details)

                        if selected_car_history:
                            display_car_info(car_details)
                        else:
                            messagebox.showinfo("Car Rental Status", "THE CAR HAS NOT BEEN RENTED YET")

                    # Define the options for the ComboBoxes

                    def create_combobox(parent_frame, x, y, options):
                        selected_condition = StringVar(value=options[0])  # Set default value
                        combo_box = Combobox(parent_frame, textvariable=selected_condition, values=options,
                                             font=(None, 10), state="readonly")
                        combo_box.place(x=x, y=y)
                        combo_box.bind("<<ComboboxSelected>>",
                                       lambda event, combo_box=combo_box: open_new_frame(combo_box.get(), parent_frame))

                    fine_amounts = {
                        "Dents": 2000, "Scratches": 1000, "Fender Benders": 5000, "Tyre Cuts": 500, "Punctures": 200,
                        "Suspension Damage": 3000, "Stains": 1200, "Tears": 700, "Trims": 600, "Torn Blades": 500,
                        "Cracked Blades": 1000, "Split Blades": 1400, "Burnout Bulbs": 500, "Cracked Lens": 1500,
                        "Uneven Lighting": 500, "Low Fluid Levels": 500, "Fluid Leaks": 1000,
                        "Fluid Contamination": 700
                    }

                    def open_new_frame(option, parent_frame):
                        global total_fine
                        options = {
                            "1": ["Dents", "Scratches", "Fender Benders", "None"],
                            "2": ["Tyre Cuts", "Punctures", "Suspension Damage", "None"],
                            "3": ["Stains", "Tears", "Trims", "None"],
                            "4": ["Torn Blades", "Cracked Blades", "Split Blades", "None"],
                            "5": ["Burnout Bulbs", "Cracked Lens", "Uneven Lighting", "None"],
                            "6": ["Low Fluid Levels", "Fluid Leaks", "Fluid Contamination", "None"]
                        }
                        if option and option != "None":
                            print(option)
                            option_str = option[0] if isinstance(option, list) else option  # Ensure option is a string

                            # Create a new frame for the selected option
                            new_frame = Frame(parent_frame, width=550, height=350, bg='#e3eeff', highlightthickness=3,
                                              borderwidth=3, highlightcolor='Black', highlightbackground='black')
                            new_frame.place(x=550, y=200)

                            # Damage description label and listbox
                            damage_label = Label(new_frame, text="Damage Description", font=('arial', 18, 'bold'),
                                                 bg='#e3eeff')
                            damage_label.place(x=180, y=10)

                            damage_listbox = Text(new_frame, bg='white', width=45, height=5, highlightthickness=0,
                                                  borderwidth=1, font=("Helvetica", 12))
                            damage_listbox.place(x=75, y=60)  # Adjust the position as needed

                            # Fine amount label
                            fine_amount_label = Label(new_frame, text="Fine Amount", font=('arial', 16), bg='#e3eeff')
                            fine_amount_label.place(x=230, y=170)

                            # Calculate fine amount based on selected option
                            fine_amount = fine_amounts.get(option_str, 0)
                            fine_label = Label(new_frame, text=str(fine_amount) + " RUPEES", font=('arial', 14),
                                               fg='red',
                                               bg='#e3eeff')
                            fine_label.place(x=220, y=215)

                            # Pay fine button
                            pay_fine_button = Button(new_frame, text="Pay Fine", fg='white', bg='green', font='10',
                                                     command=lambda: pay_fine(fine_amount, new_frame))
                            pay_fine_button.place(x=240, y=290)
                            total_fine += fine_amount
                            print(total_fine)
                        else:
                            print(option)
                            print(total_fine)

                    def pay_fine(amount, frame):
                        # Display message box
                        messagebox.showinfo("Fine Paid", "Fine of {} INR successfully paid.".format(amount))
                        # Destroy the current new frame
                        frame.destroy()

                    positions = [(100, 360), (640, 360), (1240, 360), (100, 480), (640, 480), (1240, 480)]

                    options = {
                        "1": ["Dents", "Scratches", "Fender Benders", "None"],
                        "2": ["Tyre Cuts", "Punctures", "Suspension Damage", "None"],
                        "3": ["Stains", "Tears", "Trims", "None"],
                        "4": ["Torn Blades", "Cracked Blades", "Split Blades", "None"],
                        "5": ["Burnout Bulbs", "Cracked Lens", "Uneven Lighting", "None"],
                        "6": ["Low Fluid Levels", "Fluid Leaks", "Fluid Contamination", "None"]
                    }
                    # Create and place six ComboBoxes
                    for i, (x, y) in enumerate(positions):
                        create_combobox(recieve_cars_frame, x, y, options[str(i + 1)])

                    search_car_button = Button(recieve_cars_frame, text="Search", fg='white', bg='#1b87d2', width=6,
                                               font=("yu gothic ui bold", 16), command=lambda: display_recive_car_info
                        (car_id_entry.get()))
                    search_car_button.place(x=1380, y=8)

                    recieve_back_button = Button(recieve_cars_frame, text="Receive Car", fg='white', bg='#1b87d2',
                                                 width=12, font=("yu gothic ui bold", 16), command=lambda: take_car_back
                        (car_id_entry.get()))
                    recieve_back_button.place(x=680, y=580)

                    label1 = Label(recieve_cars_frame, text="RECIEVE BACK CAR", font=("Helvetica", 19, 'bold'),
                                   bg="#4e4f4f", fg='yellow')
                    label1.place(relx=0.5, rely=0.03, anchor="center")

                    label1 = Label(recieve_cars_frame, text="BOOKING DETAILS", font=("Helvetica", 19, 'bold'),
                                   bg="#4e4f4f", fg='white')
                    label1.place(x=680, y=70)

                    car_id_label = Label(recieve_cars_frame, text="Enter Car Id ", font=("Helvetica", 19, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_id_label.place(relx=0.7, rely=0.03, anchor="center")
                    car_id_entry = Entry(recieve_cars_frame, width=7, fg="black", font=("yu gothic ui semibold", 12),
                                         highlightthickness=2)
                    car_id_entry.place(x=1240, y=8)

                    car_name_label = Label(recieve_cars_frame, text="Car Name ", font=("Helvetica", 19, 'bold'),
                                           bg="#4e4f4f", fg='white')
                    car_name_label.place(x=20, y=130)

                    car_no_label = Label(recieve_cars_frame, text="Car Number ", font=("Helvetica", 19, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=275, y=130)

                    car_no_label = Label(recieve_cars_frame, text="Customer Name", font=("Helvetica", 19, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=490, y=130)

                    car_no_label = Label(recieve_cars_frame, text="Customer Number", font=("Helvetica", 19, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=760, y=130)

                    car_no_label = Label(recieve_cars_frame, text="Pick-up Date", font=("Helvetica", 19, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=1050, y=130)

                    car_no_label = Label(recieve_cars_frame, text="Drop-off Date", font=("Helvetica", 19, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=1280, y=130)

                    line1 = Canvas(recieve_cars_frame, width=1600, height=3, bg='white', borderwidth=0)
                    line1.place(x=0, y=235)

                    label1 = Label(recieve_cars_frame, text="VEHICLE INSPECTION", font=("Helvetica", 19, 'bold'),
                                   bg="#4e4f4f", fg='yellow')
                    label1.place(x=675, y=250)

                    car_no_label = Label(recieve_cars_frame, text="1. Is the Car's exterior condition good?",
                                         font=("Helvetica", 15, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=10, y=310)

                    car_no_label = Label(recieve_cars_frame, text="2. Are there any damages or issues with the wheels "
                                                                  "and tires?", font=("Helvetica", 15, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=450, y=310)
                    car_no_label = Label(recieve_cars_frame, text="3. Is the interior of the car in good condition?",
                                         font=("Helvetica", 15, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=1090, y=310)
                    car_no_label = Label(recieve_cars_frame, text="4. Do the windshield wipers operate correctly?",
                                         font=("Helvetica", 15, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=5, y=430)

                    car_no_label = Label(recieve_cars_frame, text="5. Are the indicators, taillights and headlights are"
                                                                  "working properly?", font=("Helvetica", 15, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=450, y=430)

                    car_no_label = Label(recieve_cars_frame,
                                         text="6. Are there any fluid leaks under the vehicle?",
                                         font=("Helvetica", 15, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=1090, y=430)

                recieve_car_image = PhotoImage(file="images/recieve_back_car.png")
                recieve_car_button = Button(admin_main_dashframe, image=recieve_car_image, compound="top", bg="pink",
                                            text="Recieve Back Car", font=("arial", 16), cursor='hand2',
                                            command=recieve_back_cars)
                recieve_car_button.image = recieve_car_image
                recieve_car_button.place(x=882, y=150, width=220, height=158)

                def display_car_details1(available_cars_frame):
                    connection = sqlite3.connect("Car_Rental_Management_Database.db")
                    cur = connection.cursor()
                    cur.execute("SELECT * FROM Cars_info LIMIT 12")
                    all_cars_list = cur.fetchall()
                    cur.execute("SELECT * FROM Rented_car_list")
                    rented_list = cur.fetchall()

                    label_characteristics = {
                        "font": ("Helvetica", 12),
                        "bg": "#4e4f4f",
                        "fg": "white"
                    }

                    # Create labels dynamically for each available car
                    for i, car_info in enumerate(all_cars_list):
                        labels_info = [
                            {"text": car_info[0], "x": 30},
                            {"text": car_info[1], "x": 155},
                            {"text": car_info[2], "x": 340},
                            {"text": car_info[3], "x": 570},
                            {"text": car_info[4], "x": 790},
                            {"text": car_info[7], "x": 990},
                            {"text": car_info[8], "x": 1175},
                            {"text": "Available", "x": 1350, "color": "#03fc45"}
                        ]

                        # Create labels dynamically for each characteristic of available cars
                        for j, label_info in enumerate(labels_info):
                            label_characteristics_local = label_characteristics.copy()
                            if "color" in label_info and label_info["text"] == "Available":
                                label_characteristics_local["fg"] = label_info["color"]
                            label = Label(available_cars_frame, text=label_info["text"], **label_characteristics_local)
                            label.place(x=label_info["x"], y=108 + i * 40)

                    # Calculate the starting y position for rented cars labels
                    rented_start_y = 108 + len(all_cars_list) * 40  # Add some extra space for separation

                    # Create labels dynamically for each rented car
                    for i, rented_car_info in enumerate(rented_list):
                        rented_labels_info = [
                            {"text": rented_car_info[0], "x": 30},
                            {"text": rented_car_info[1], "x": 155},
                            {"text": rented_car_info[2], "x": 340},
                            {"text": rented_car_info[3], "x": 570},
                            {"text": rented_car_info[4], "x": 790},
                            {"text": rented_car_info[7], "x": 990},
                            {"text": rented_car_info[8], "x": 1175},
                            {"text": "Rented", "x": 1350, "color": "#f24441"}
                        ]

                        # Create labels dynamically for each characteristic of rented cars
                        for j, rented_label_info in enumerate(rented_labels_info):
                            label_characteristics_local = label_characteristics.copy()
                            if "color" in rented_label_info and rented_label_info["text"] == "Rented":
                                label_characteristics_local["fg"] = rented_label_info["color"]
                            label = Label(available_cars_frame, text=rented_label_info["text"],
                                          **label_characteristics_local)
                            label.place(x=rented_label_info["x"], y=rented_start_y + i * 40)

                    total_cars = Label(available_cars_frame, text="Total Cars: " + str(len(all_cars_list) + len
                    (rented_list)), font=("Helvetica", 17, 'bold'), bg="#4e4f4f", fg='yellow')
                    total_cars.place(x=30, y=600)

                    current_cars = Label(available_cars_frame, text="Available Cars: " + str(len(all_cars_list)),
                                         font=("Helvetica", 17, 'bold'), bg="#4e4f4f", fg='yellow')
                    current_cars.place(x=370, y=600)

                    rent_cars = Label(available_cars_frame, text="Rented Cars: " + str(len(rented_list)),
                                      font=("Helvetica", 17, 'bold'), bg="#4e4f4f", fg='yellow')
                    rent_cars.place(x=770, y=600)

                def display_car_details2(available_cars_frame):
                    connection = sqlite3.connect("Car_Rental_Management_Database.db")
                    cur = connection.cursor()
                    cur.execute("SELECT * FROM Cars_info LIMIT 12 OFFSET 12")
                    all_cars_list = cur.fetchall()
                    cur.execute("SELECT * FROM Rented_car_list")
                    rented_list = cur.fetchall()
                    print("ALL RENTED VEHICLES =", rented_list)

                    label_characteristics = {
                        "font": ("Helvetica", 12),
                        "bg": "#4e4f4f",
                        "fg": "white"
                    }

                    # Create labels dynamically for each available car
                    for i, car_info in enumerate(all_cars_list):
                        labels_info = [
                            {"text": car_info[0], "x": 30},
                            {"text": car_info[1], "x": 155},
                            {"text": car_info[2], "x": 340},
                            {"text": car_info[3], "x": 570},
                            {"text": car_info[4], "x": 790},
                            {"text": car_info[7], "x": 990},
                            {"text": car_info[8], "x": 1175},
                            {"text": "Available", "x": 1350, "color": "#03fc45"}
                        ]

                        # Create labels dynamically for each characteristic of available cars
                        for j, label_info in enumerate(labels_info):
                            label_characteristics_local = label_characteristics.copy()
                            if "color" in label_info and label_info["text"] == "Available":
                                label_characteristics_local["fg"] = label_info["color"]
                            label = Label(available_cars_frame, text=label_info["text"], **label_characteristics_local)
                            label.place(x=label_info["x"], y=108 + i * 40)

                    # Calculate the starting y position for rented cars labels
                    rented_start_y = 108 + len(all_cars_list) * 40  # Add some extra space for separation

                    # Create labels dynamically for each rented car
                    for i, rented_car_info in enumerate(rented_list):
                        rented_labels_info = [
                            {"text": rented_car_info[0], "x": 30},
                            {"text": rented_car_info[1], "x": 155},
                            {"text": rented_car_info[2], "x": 340},
                            {"text": rented_car_info[3], "x": 570},
                            {"text": rented_car_info[4], "x": 790},
                            {"text": rented_car_info[7], "x": 990},
                            {"text": rented_car_info[8], "x": 1175},
                            {"text": "Rented", "x": 1350, "color": "#f24441"}
                        ]

                        # Create labels dynamically for each characteristic of rented cars
                        for j, rented_label_info in enumerate(rented_labels_info):
                            label_characteristics_local = label_characteristics.copy()
                            if "color" in rented_label_info and rented_label_info["text"] == "Rented":
                                label_characteristics_local["fg"] = rented_label_info["color"]
                            label = Label(available_cars_frame, text=rented_label_info["text"],
                                          **label_characteristics_local)
                            label.place(x=rented_label_info["x"], y=rented_start_y + i * 40)

                    total_cars = Label(available_cars_frame, text="Total Cars: " + str(len(all_cars_list) + len
                    (rented_list)), font=("Helvetica", 17, 'bold'), bg="#4e4f4f", fg='yellow')
                    total_cars.place(x=30, y=600)

                    current_cars = Label(available_cars_frame, text="Available Cars: " + str(len(all_cars_list)),
                                         font=("Helvetica", 17, 'bold'), bg="#4e4f4f", fg='yellow')
                    current_cars.place(x=370, y=600)

                    rent_cars = Label(available_cars_frame, text="Rented Cars: " + str(len(rented_list)),
                                      font=("Helvetica", 17, 'bold'), bg="#4e4f4f", fg='yellow')
                    rent_cars.place(x=770, y=600)

                def available_cars_2():  # function to see all the available cars in the system
                    avaiable_cars_frame2 = Frame(admin_main_dashframe, width=1600, height=700, background="white")
                    avaiable_cars_frame2.place(x=0, y=310)

                    canvas = Canvas(avaiable_cars_frame2, width=1600, height=650, background="#4e4f4f")
                    canvas.pack()

                    label1 = Label(canvas, text="All Cars", font=("Helvetica", 22, 'bold'),
                                   bg="#4e4f4f", fg='yellow')
                    label1.place(relx=0.5, rely=0.03, anchor="center")

                    # Draw a horizontal line from (x1, y1) to (x2, y2)
                    canvas.create_line(10, 50, 1470, 50, width=2, fill="black")
                    canvas.create_line(10, 105, 1470, 105, width=2, fill="black")
                    canvas.create_line(10, 50, 10, 575, width=2, fill="black")
                    canvas.create_line(1470, 50, 1470, 575, width=2, fill="black")
                    canvas.create_line(100, 50, 100, 575, width=2, fill="black")
                    canvas.create_line(310, 50, 310, 575, width=2, fill="black")
                    canvas.create_line(510, 50, 510, 575, width=2, fill="black")
                    canvas.create_line(700, 50, 700, 575, width=2, fill="black")
                    canvas.create_line(930, 50, 930, 575, width=2, fill="black")
                    canvas.create_line(1120, 50, 1120, 575, width=2, fill="black")
                    canvas.create_line(1300, 50, 1300, 575, width=2, fill="black")

                    car_id_label = Label(avaiable_cars_frame2, text="Car Id", font=("Helvetica", 15, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_id_label.place(x=25, y=65)

                    canvas.create_line(10, 145, 1470, 145, width=2, fill="black")

                    car_name_label = Label(avaiable_cars_frame2, text="Car Number", font=("Helvetica", 15, 'bold'),
                                           bg="#4e4f4f", fg='white')
                    car_name_label.place(x=160, y=68)
                    canvas.create_line(10, 180, 1470, 180, width=2, fill="black")

                    car_no_label = Label(avaiable_cars_frame2, text="Car Name", font=("Helvetica", 15, 'bold'),
                                         bg="#4e4f4f", fg='white')
                    car_no_label.place(x=340, y=65)
                    canvas.create_line(10, 215, 1470, 215, width=2, fill="black")

                    seats_label = Label(avaiable_cars_frame2, text="Seats Capacity", font=("Helvetica", 15, 'bold'),
                                        bg="#4e4f4f", fg='white')
                    seats_label.place(x=530, y=65)
                    canvas.create_line(10, 255, 1470, 255, width=2, fill="black")

                    luggage_label = Label(avaiable_cars_frame2, text="Luggage Capacity", font=("Helvetica", 15, 'bold'),
                                          bg="#4e4f4f", fg='white')
                    luggage_label.place(x=740, y=65)
                    canvas.create_line(10, 295, 1470, 295, width=2, fill="black")

                    type_label = Label(avaiable_cars_frame2, text="Car Type", font=("Helvetica", 15, 'bold'),
                                       bg="#4e4f4f", fg='white')
                    type_label.place(x=990, y=65)
                    canvas.create_line(10, 335, 1470, 335, width=2, fill="black")

                    rent_label = Label(avaiable_cars_frame2, text="Car Rent", font=("Helvetica", 15, 'bold'),
                                       bg="#4e4f4f", fg='white')
                    rent_label.place(x=1170, y=65)
                    canvas.create_line(10, 375, 1470, 375, width=2, fill="black")

                    availability_label = Label(avaiable_cars_frame2, text="Availability",
                                               font=("Helvetica", 15, 'bold'),
                                               bg="#4e4f4f", fg='white')
                    availability_label.place(x=1340, y=65)
                    canvas.create_line(10, 415, 1470, 415, width=2, fill="black")

                    total_cars = Label(canvas, text="Total Cars: ", font=("Helvetica", 17, 'bold'),
                                       bg="#4e4f4f", fg='yellow')
                    total_cars.place(x=30, y=600)

                    current_cars = Label(canvas, text="Available Cars: ", font=("Helvetica", 17, 'bold'),
                                         bg="#4e4f4f", fg='yellow')
                    current_cars.place(x=370, y=600)

                    rent_cars = Label(canvas, text="Rented Cars: ", font=("Helvetica", 17, 'bold'),
                                      bg="#4e4f4f", fg='yellow')
                    rent_cars.place(x=770, y=600)

                    previous_button = Button(avaiable_cars_frame2, text="Back", fg='white', bg='#1b87d2', width=6,
                                             font=("yu gothic ui bold", 16), command=avaiable_cars_frame2.destroy)
                    previous_button.place(x=1270, y=589)

                    canvas.create_line(10, 415, 1470, 415, width=2, fill="black")
                    canvas.create_line(10, 455, 1470, 455, width=2, fill="black")
                    canvas.create_line(10, 495, 1470, 495, width=2, fill="black")
                    canvas.create_line(10, 535, 1470, 535, width=2, fill="black")
                    canvas.create_line(10, 575, 1470, 575, width=2, fill="black")

                # display_car_details2(avaiable_cars_frame2)

                def available_cars():  # function to see all the available cars in the system
                    avaiable_cars_frame = Frame(admin_main_dashframe, width=1600, height=700, background="white")
                    avaiable_cars_frame.place(x=0, y=310)

                    canvas = Canvas(avaiable_cars_frame, width=1600, height=650, background="#4e4f4f")
                    canvas.pack()

                    label1 = Label(canvas, text="All Cars", font=("Helvetica", 22, 'bold'),
                                   bg="#4e4f4f", fg='yellow')
                    label1.place(relx=0.5, rely=0.03, anchor="center")

                    # Draw a horizontal line from (x1, y1) to (x2, y2)
                    canvas.create_line(10, 50, 1470, 50, width=2, fill="black")
                    canvas.create_line(10, 105, 1470, 105, width=2, fill="black")
                    canvas.create_line(10, 50, 10, 575, width=2, fill="black")
                    canvas.create_line(1470, 50, 1470, 575, width=2, fill="black")
                    canvas.create_line(100, 50, 100, 575, width=2, fill="black")
                    canvas.create_line(310, 50, 310, 575, width=2, fill="black")
                    canvas.create_line(510, 50, 510, 575, width=2, fill="black")
                    canvas.create_line(700, 50, 700, 575, width=2, fill="black")
                    canvas.create_line(930, 50, 930, 575, width=2, fill="black")
                    canvas.create_line(1120, 50, 1120, 575, width=2, fill="black")
                    canvas.create_line(1300, 50, 1300, 575, width=2, fill="black")

                    car_id_label = Label(avaiable_cars_frame, text="Car Id", font=("Helvetica", 15, 'bold'),
                                         bg="#4e4f4f", fg='#ffffff')
                    car_id_label.place(x=25, y=65)

                    canvas.create_line(10, 145, 1470, 145, width=2, fill="black")

                    car_name_label = Label(avaiable_cars_frame, text="Car Number", font=("Helvetica", 15, 'bold'),
                                           bg="#4e4f4f", fg='#ffffff')
                    car_name_label.place(x=160, y=68)
                    canvas.create_line(10, 180, 1470, 180, width=2, fill="black")

                    car_no_label = Label(avaiable_cars_frame, text="Car Name", font=("Helvetica", 15, 'bold'),
                                         bg="#4e4f4f", fg='#ffffff')
                    car_no_label.place(x=340, y=65)
                    canvas.create_line(10, 215, 1470, 215, width=2, fill="black")

                    seats_label = Label(avaiable_cars_frame, text="Seats Capacity", font=("Helvetica", 15, 'bold'),
                                        bg="#4e4f4f", fg='#ffffff')
                    seats_label.place(x=530, y=65)
                    canvas.create_line(10, 255, 1470, 255, width=2, fill="black")

                    luggage_label = Label(avaiable_cars_frame, text="Luggage Capacity", font=("Helvetica", 15, 'bold'),
                                          bg="#4e4f4f", fg='#ffffff')
                    luggage_label.place(x=740, y=65)
                    canvas.create_line(10, 295, 1470, 295, width=2, fill="black")

                    type_label = Label(avaiable_cars_frame, text="Car Type", font=("Helvetica", 15, 'bold'),
                                       bg="#4e4f4f", fg='#ffffff')
                    type_label.place(x=990, y=65)
                    canvas.create_line(10, 335, 1470, 335, width=2, fill="black")

                    rent_label = Label(avaiable_cars_frame, text="Car Rent", font=("Helvetica", 15, 'bold'),
                                       bg="#4e4f4f", fg='#ffffff')
                    rent_label.place(x=1170, y=65)
                    canvas.create_line(10, 375, 1470, 375, width=2, fill="black")

                    availability_label = Label(avaiable_cars_frame, text="Availability", font=("Helvetica", 15, 'bold'),
                                               bg="#4e4f4f", fg='#ffffff')
                    availability_label.place(x=1340, y=65)
                    canvas.create_line(10, 415, 1470, 415, width=2, fill="black")

                    next_button = Button(avaiable_cars_frame, text="Next", fg='white', bg='#1b87d2', width=6,
                                         font=("yu gothic ui bold", 16), command=available_cars_2)
                    next_button.place(x=1270, y=589)

                    canvas.create_line(10, 415, 1470, 415, width=2, fill="black")
                    canvas.create_line(10, 455, 1470, 455, width=2, fill="black")
                    canvas.create_line(10, 495, 1470, 495, width=2, fill="black")
                    canvas.create_line(10, 535, 1470, 535, width=2, fill="black")
                    canvas.create_line(10, 575, 1470, 575, width=2, fill="black")

                    display_car_details1(avaiable_cars_frame)

                available_cars_image = PhotoImage(file="images/available_cars.png")
                available_cars_button = Button(admin_main_dashframe, image=available_cars_image, compound="top",
                                               bg="pink", text="All Cars", font=("arial", 16), cursor='hand2',
                                               command=available_cars)
                available_cars_button.image = available_cars_image
                available_cars_button.place(x=1102, y=150, width=220, height=158)

                logout_image = PhotoImage(file="images/logout.png")
                logout_button = Button(admin_main_dashframe, image=logout_image, compound="top", bg="pink",
                                       text="Logout", font=("arial", 16), cursor='hand2', command=logout)
                logout_button.image = logout_image
                logout_button.place(x=1322, y=150, width=220, height=158)

                available_cars()

            design_frame1 = Listbox(admin_frame, bg='#0c71b9', width=180, height=60, highlightthickness=0,
                                    borderwidth=0)
            design_frame1.place(x=0, y=0)

            design_frame2 = Listbox(admin_frame, bg='#1e85d0', width=150, height=60, highlightthickness=0,
                                    borderwidth=0)
            design_frame2.place(x=676, y=0)

            design_frame3 = Listbox(admin_frame, bg='#1e85d0', width=105, height=38, highlightthickness=0,
                                    borderwidth=0)
            design_frame3.place(x=75, y=106)

            design_frame4 = Listbox(admin_frame, bg='#f8f8f8', width=100, height=38, highlightthickness=0,
                                    borderwidth=0)
            design_frame4.place(x=676, y=106)

            # ====== User_id ====================
            userid = Entry(design_frame4, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2)
            userid.place(x=134, y=195, width=256, height=34)
            userid.config(highlightbackground="black", highlightcolor="black")

            email_label = Label(design_frame4, text='• Userid', fg="black", bg='#f8f8f8',
                                font=("yu gothic ui", 11, 'bold'))
            email_label.place(x=139, y=160)

            # ==== Password ==================
            password_entry2 = Entry(design_frame4, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•',
                                    highlightthickness=2)
            password_entry2.place(x=134, y=285, width=256, height=34)
            password_entry2.config(highlightbackground="black", highlightcolor="black")

            password_label = Label(design_frame4, text='• Password', fg="black", bg='#f8f8f8',
                                   font=("yu gothic ui", 11, 'bold'))
            password_label.place(x=139, y=250)

            # function for show and hide password
            def password_command():
                if password_entry2.cget('show'):
                    password_entry2.config(show='')
                else:
                    password_entry2.config(show='•')

            def login():
                userid_value = userid.get()
                password_value = password_entry2.get()

                # Check if both fields are filled
                if not userid_value or not password_value:
                    messagebox.showerror("Error", "Please enter both User ID and Password.")
                    return

                # Check if the credentials are correct
                if userid_value == 'admin' and password_value == 'admin@123':
                    messagebox.showinfo("Success", "Login Successful!")
                    admin_dashboard()
                else:
                    messagebox.showerror("Error", "Incorrect userid or password")

            # ====== checkbutton ==============
            checkButton = Checkbutton(design_frame4, bg='#f8f8f8', command=password_command, text='Show password')
            checkButton.place(x=140, y=350)

            # ===== Welcome Label ==============
            welcome_admin_label = Label(design_frame4, text='WELCOME ADMIN', font=('Arial', 19, 'bold'), bg='#f8f8f8')
            welcome_admin_label.place(x=138, y=15)

            # ======= top Login Button =========
            login_label = Label(admin_frame, text='LOGIN', font=("yu gothic ui bold", 14), bg='#f8f8f8', fg="black",
                                borderwidth=0, activebackground='#1b87d2')
            login_label.place(x=888, y=195)

            login_line = Canvas(admin_frame, width=150, height=5, bg='#1b87d2')
            login_line.place(x=840, y=229)

            loginBtn = Button(design_frame4, fg='Black', text='LOGIN', bg='#1b87d2', font=("yu gothic ui bold", 15),
                              cursor='hand2', activebackground='#1b87d2', command=login)
            loginBtn.place(x=133, y=400, width=256, height=50)

            # ======= ICONS =================
            # ===== User_id icon =========
            userid_icon = Image.open('images/user.png')
            user_photo = ImageTk.PhotoImage(userid_icon)
            userid_icon_label = Label(design_frame4, image=user_photo, bg='#f8f8f8')
            userid_icon_label.image = user_photo
            userid_icon_label.place(x=86, y=189)

            # ===== password icon =========
            password_icon = Image.open('images/pass.png')
            password_photo = ImageTk.PhotoImage(password_icon)
            password_icon_label = Label(design_frame4, image=password_photo, bg='#f8f8f8')
            password_icon_label.image = password_photo
            password_icon_label.place(x=86, y=280)

            # ===== picture icon =========
            picture_icon = Image.open('images/admin2.png')
            admin_photo = ImageTk.PhotoImage(picture_icon)
            picture_icon_label = Label(design_frame4, image=admin_photo, bg='#f8f8f8')
            picture_icon_label.image = admin_photo
            picture_icon_label.place(x=373, y=7)

            # ===== Left Side Picture ============
            side_image = Image.open('images/car_rent.png')
            photo = ImageTk.PhotoImage(side_image)
            side_image_label = Label(design_frame3, image=photo, bg='#1e85d0')
            side_image_label.image = photo
            side_image_label.place(x=50, y=30)

            # Create a button to go back to the main window
            back_button = Button(design_frame4, fg='Black', bg='#d65af2', font=("yu gothic ui bold", 12), cursor='hand2'
                                 , activebackground='#d65af2', text="BACK TO MAIN",
                                 command=lambda: show_main_window("admin"))
            back_button.pack()
            back_button.place(x=169, y=490, width=180, height=40)

            # Hide other frames
            if frame1 is not None:
                frame1.pack_forget()
            if frame2 is not None:
                frame2.pack_forget()
            admin_frame.pack(fill="both", expand=True)

    def show_main_window(from_page):
        global customer_frame, admin_frame
        if customer_frame is not None:
            customer_frame.pack_forget()
            customer_frame = None
        if admin_frame is not None:
            admin_frame.pack_forget()
            admin_frame = None
        if frame1 is not None:
            frame1.pack(side="left", fill="both", expand=True)
        if frame2 is not None:
            frame2.pack(side="right", fill="both", expand=True)

    def on_enter(event):
        event.widget.config(bg="#736767")

    def on_leave(event):
        event.widget.config(bg="white")

    def setup_button(button, clicked_command):
        button.configure(bg="white", font=("arial", 18), relief="solid", command=clicked_command)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    # Display image buttons with labels
    customer_button = Button(frame2, image=customer_image, text="Customer", compound="top", bg="white",
                             command=customer_clicked, font=("arial", 18), borderwidth=0)
    customer_button.image = customer_image
    setup_button(customer_button, customer_clicked)
    customer_button.pack(pady=10)
    customer_button.place(x=190, y=210, width=240, height=235)

    customer_button.bind("<Enter>", on_enter)
    customer_button.bind("<Leave>", on_leave)

    admin_button = Button(frame2, image=admin_image, text="Admin", compound="top", font=("arial", 18), bg="white",
                          command=admin_clicked, background='white', borderwidth=0)
    admin_button.image = admin_image
    setup_button(admin_button, admin_clicked)

    admin_button.pack(pady=10)
    admin_button.place(x=190, y=550, width=240, height=230)

    # Run the Tkinter event loop
    window.mainloop()


file_name = "car_data.txt"

# Check if the file exists
if not os.path.exists(file_name):
    # Create a dictionary to store the data
    car_data = {
        "new_car": new_car,
        "removed_car": removed_car
    }

    # Write the dictionary to the file
    with open(file_name, "w") as file:
        for key, value in car_data.items():
            file.write(f"{key}: {value}\n")
    print("Data saved to 'car_data.txt' file.")
else:
    print("'car_data.txt' file already exists. Skipping writing data.")

# Call the function to create the divided page
create_divided_page()
