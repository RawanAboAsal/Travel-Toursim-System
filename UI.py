import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

from graph import *
from attraction import *
from booking import *

class UI:
    def __init__(self, master):
        self.master = master
        self.fullscreen = False
        self.DisplayHomePage()

    def DisplayHomePage(self):
        
        if not self.fullscreen:
            self.master.attributes('-fullscreen', True) 
            self.fullscreen = True
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))


        # Load and display the background image
        bg_image = Image.open("assets/home.png")
        resized_bg = bg_image.resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()), Image.LANCZOS)
        
        
        tkbg_image = ImageTk.PhotoImage(resized_bg)
        self.bg_image_label = tk.Label(self.master, image=tkbg_image)
        self.bg_image_label.image = tkbg_image
        self.bg_image_label.place(relx=0.5, rely=0.5, anchor='center')

        
        
     

        # Itinerary Planning Button
        self.itenaryButton = tk.Button(self.master, text="Itinerary Planning", font=("Verdana", 27, "bold"), highlightbackground="#0d2143", highlightthickness=0, borderwidth=0,
                                        command=self.InitializeItineraryPlanningPage, fg="#00ffa3", bg="#0d2243")
        self.itenaryButton.place(relx=0.035, rely=0.5, anchor='w')

        # Booking Management Button
        self.bookingManagementButton = tk.Button(self.master, text="Booking Management", relief="flat", highlightbackground="#0d2143", 
                                                 highlightthickness=0, borderwidth=0, font=("Verdana", 27, "bold"), command=self.InitializeBookingManagementPage, fg="#00ffa3", bg="#0d2243")
        self.bookingManagementButton.place(relx=0.035, rely=0.6, anchor='w')

        # Attraction Management Button
        self.attractionManagementButton = tk.Button(self.master, text="Attraction Management", relief="flat", highlightbackground="#0d2143", 
                                                    highlightthickness=0, borderwidth=0, font=("Verdana", 27, "bold"), command=self.InitializeAttractionManagementPage, fg="#00ffa3", bg="#0d2243")
        self.attractionManagementButton.place(relx=0.035, rely=0.7, anchor='w')
        
        

        self.attractionTitle = None
        self.addAttractionButton = None
        self.getAllAttractionsButton = None
        self.addFeedbackButton = None
        
        def close_window():
            self.master.destroy() 
            
        self.close_button = tk.Button(self.master, text="x", relief="flat", highlightbackground="#0d2143", 
                                    highlightthickness=0, borderwidth=0, font=("Verdana", 37, "bold"), command=close_window, fg="#00ffa3", bg="#0d2243")
        self.close_button.place(relx=1.01, rely=-0.035, anchor='ne')

          # Adjust the position as needed

        self.bookingInstance = HotelBookingSystem()


    def DisableHomePage(self):
        if self.fullscreen:
            self.master.attributes('-fullscreen', False)  # Disable full-screen mode
            self.fullscreen = False
      
        self.itenaryButton.place_forget()
        self.bookingManagementButton.place_forget()
        self.attractionManagementButton.place_forget()
        self.bg_image_label.place_forget()
        self.close_button.place_forget()
        

    def InitializeItineraryPlanningPage(self):
        self.DisableHomePage()
        self.master.attributes('-fullscreen', True)  # Open in full-screen mode
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))

        # Configure the window background color
        self.master.configure(bg="#0d2143")
        
        def close_window():
            self.master.destroy() 
            
        self.close_button = tk.Button(self.master, text="x", relief="flat", highlightbackground="#0d2143", 
                                    highlightthickness=0, borderwidth=0, font=("Verdana", 37, "bold"), command=close_window, fg="#00ffa3", bg="#0d2243")
        self.close_button.place(relx=1.01, rely=-0.035, anchor='ne')
       
        self.ItineraryTitle = tk.Label(self.master, text="Itinerary Planning", font=("Verdana", 40, "bold"), fg="#00ffa3", bg="#0d2143")
        self.ItineraryTitle.place(relx=0.5, rely=0.04, anchor='center')
    
        list_of_cities = ["Company", "Hurghada", "Sharm el Sheikh", "Alexandria", "North Coast", "El Gouna", "North Sinai", "Luxor", "El Mazarita", "Aswan", "Port Said"]

        self.starting_city_label = tk.Label(self.master, text="The shortest distance from ", font=("Arial", 17), fg="#00ffa3", bg="#0d2143")
        self.starting_city_label.place(relx=0.015, rely=0.1)
        
        self.starting_city_combobox = ttk.Combobox(self.master, values=list_of_cities, width=15)
        self.starting_city_combobox.place(relx=0.2, rely=0.105)

        self.destination_label = tk.Label(self.master, text="to", font=("Arial", 17), fg="#00ffa3", bg="#0d2143")
        self.destination_label.place(relx=0.277, rely=0.1)
        
        self.destination_combobox = ttk.Combobox(self.master, values=list_of_cities, width=15)
        self.destination_combobox.place(relx=0.297, rely=0.105)
        
        self.is_label = tk.Label(self.master, text="is:", font=("Arial", 17), fg="#00ffa3", bg="#0d2143")
        self.is_label.place(relx=0.373, rely=0.1)

        self.calculate_button = tk.Button(self.master, text="Calculate Shortest Path", command=self.DisplayShortestPath, font=("Arial", 15), fg="#00ffa3", bg="#0d2143")
        self.calculate_button.place(relx=0.9, rely=0.11, anchor='center')

        self.shortest_path_info = tk.Label(self.master, text="", font=("Arial", 17, "bold"), fg="#00ffa3", bg="#0d2143")
        self.shortest_path_info.place(relx=0.39, rely=0.1)

        self.back_button = tk.Button(self.master, text="Back to Home", command=self.CloseItineraryPlanningPage, font=("Arial", 15), fg="#00ffa3", bg="#0d2143")
        self.back_button.place(relx=0, rely=0)

        image = Image.open("assets/graphf4.png")
        resize_image = image.resize((1930, 840))
        tk_image = ImageTk.PhotoImage(resize_image)
        self.image_label = tk.Label(self.master, image=tk_image, bg='#0d2143')
        self.image_label.image = tk_image
        self.image_label.place(relx=0.45, rely=0.62, anchor='center')

    def DisplayShortestPath(self):
        start_city = self.starting_city_combobox.get()
        destination = self.destination_combobox.get()
        
        g = Graph()  # Create the graph
        # Add edges to the graph (your edges adding code here)
        
        co = "Company"
        hu = "Hurghada"
        sh = "Sharm el Sheikh"
        al = "Alexandria"
        nc = "North Coast"
        go = "El Gouna"
        ns = "North Sinai"
        lu = "Luxor"
        maz = "El Mazarita"
        asw = "Aswan"
        ps = "Port Said"

        g.add_edge(co, go, 443)
        g.add_edge(go, hu, 32)
        g.add_edge(hu, go, 32)
        g.add_edge(go, co, 445)
        
        g.add_edge(hu, lu, 309)
        g.add_edge(lu, hu, 304)
        
        g.add_edge(co, sh, 502)
        g.add_edge(sh, co, 506)
        g.add_edge(co, ns, 263)
        g.add_edge(ns, co, 263)
        g.add_edge(co, ps, 200)
        g.add_edge(ps, co, 196)
        g.add_edge(ns, ps, 246)
        g.add_edge(ps, ns, 237)
        g.add_edge(ns, sh, 437)
        g.add_edge(sh, ns, 427)
        
        g.add_edge(co, lu, 658)
        g.add_edge(lu, maz, 65)
        g.add_edge(maz, asw, 40)
        g.add_edge(asw, maz, 40)
        g.add_edge(maz, lu, 65)
        g.add_edge(lu, co, 653)
        
        g.add_edge(co, al, 218)
        g.add_edge(al, nc, 64)
        g.add_edge(nc, al, 70)
        g.add_edge(al, co, 219)
        
        distances = dijkstra(g, start_city)  # Run Dijkstra's algorithm

        shortest_distance = distances.get(destination, float('inf'))
        if not start_city and not destination:
            self.shortest_path_info.config(text=f"(Please select the start and destination cities)")
        elif not start_city:
            self.shortest_path_info.config(text=f"(Please select the city you want to start from)")
        elif not destination:
            self.shortest_path_info.config(text=f"(Please select the city you want to go to (destination) )")
        elif shortest_distance == 0:
            self.shortest_path_info.config(text=f"(you are already in {start_city})")
        elif shortest_distance != float('inf'):
            self.shortest_path_info.config(text=f"{shortest_distance} km")       
        else:
            self.shortest_path_info.config(text=f" Please enter right inputs for the cities (Choose from the combobox :)")
                 
    def CloseItineraryPlanningPage(self):
        self.master.configure(bg="#FFFFFF")
        self.back_button.place_forget()
        self.ItineraryTitle.place_forget()
        self.starting_city_label.place_forget()
        self.starting_city_combobox.place_forget()
        self.destination_label.place_forget()
        self.is_label.place_forget()
        self.destination_combobox.place_forget()
        self.calculate_button.place_forget()
        self.image_label.place_forget()
        if self.shortest_path_info:
            self.shortest_path_info.place_forget()
        self.DisplayHomePage()

    def InitializeBookingManagementPage(self):
        self.DisableHomePage()
        self.master.geometry("500x350")
        

        self.bookingTitle = tk.Label(self.master, text = "Booking Management")
        self.bookingTitle.place(relx = 0.5, rely = 0.1, anchor = 'center')
        self.addbookingButton = tk.Button(self.master, text="Add Booking", command=self.InitializeAddBookingsPage)
        self.addbookingButton.place(relx = 0.5, rely = 0.25, anchor = 'center')
        self.getbookingsButton = tk.Button(self.master, text="Get Bookings", command=self.InitializeGetAllBookingsPage)
        self.getbookingsButton.place(relx = 0.5, rely = 0.35, anchor = 'center')
        self.closebookingsButton = tk.Button(self.master, text="Back", command=self.CloseBookingManagementPage)
        self.closebookingsButton.place(relx = 0.5, rely = 0.85, anchor = 'center')
        
        
    def CloseBookingManagementPage(self):
        self.bookingTitle.place_forget()
        self.addbookingButton.place_forget()
        self.getbookingsButton.place_forget()
        self.closebookingsButton.place_forget()
        self.DisplayHomePage()

    def InitializeAddBookingsPage(self):
        self.bookingTitle.place_forget()
        self.addbookingButton.place_forget()
        self.getbookingsButton.place_forget()
        self.closebookingsButton.place_forget()

        self.booking_city_label = ttk.Label(self.master, text="City:")
        self.booking_city_label.grid(row=0, column=0, padx=10, pady=5)
        self.booking_city_combobox = ttk.Combobox(self.master, values=self.bookingInstance.hotels_data['location'].unique().tolist(), state="readonly")
        self.booking_city_combobox.grid(row=0, column=1, padx=10, pady=5)

        self.booking_room_type_label = ttk.Label(self.master, text="Room Type:")
        self.booking_room_type_label.grid(row=1, column=0, padx=10, pady=5)
        self.booking_room_type_combobox = ttk.Combobox(self.master, values=['Standard', 'Deluxe', 'Executive_Suite', 'Single', 'Double', 'Family_Suite', 'Triple'], state="readonly")
        self.booking_room_type_combobox.grid(row=1, column=1, padx=10, pady=5)

        self.booking_rooms_label = ttk.Label(self.master, text="Number of Rooms:")
        self.booking_rooms_label.grid(row=2, column=0, padx=10, pady=5)
        self.booking_rooms_entry = ttk.Entry(self.master)
        self.booking_rooms_entry.grid(row=2, column=1, padx=10, pady=5)

        self.booking_beds_label = ttk.Label(self.master, text="Number of Beds:")
        self.booking_beds_label.grid(row=3, column=0, padx=10, pady=5)
        self.booking_beds_entry = ttk.Entry(self.master)
        self.booking_beds_entry.grid(row=3, column=1, padx=10, pady=5)

        self.booking_name_label = ttk.Label(self.master, text="Your Name:")
        self.booking_name_label.grid(row=4, column=0, padx=10, pady=5)
        self.booking_name_entry = ttk.Entry(self.master)
        self.booking_name_entry.grid(row=4, column=1, padx=10, pady=5)

        self.booking_nights_label = ttk.Label(self.master, text="Number of Nights:")
        self.booking_nights_label.grid(row=5, column=0, padx=10, pady=5)
        self.booking_nights_entry = ttk.Entry(self.master)
        self.booking_nights_entry.grid(row=5, column=1, padx=10, pady=5)

        self.booking_submit_button = ttk.Button(self.master, text="Submit Booking", command=self.submit_booking)
        self.booking_submit_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.booking_back_button = ttk.Button(self.master, text="back", command=self.CloseAddBookingPage)
        self.booking_back_button.grid(row=7, column=1, columnspan=2, pady=10)

    def submit_booking(self):
        chosen_city = self.booking_city_combobox.get()
        chosen_room_type = self.booking_room_type_combobox.get()
        num_rooms = self.booking_rooms_entry.get()
        num_beds = self.booking_beds_entry.get()
        customer_name = self.booking_name_entry.get()
        num_nights = self.booking_nights_entry.get()

        # Check for empty fields
        if not all([chosen_city, chosen_room_type, num_rooms, num_beds, customer_name, num_nights]):
            print("Please fill in all the fields.")
            return

        # Check if num_rooms, num_beds, and num_nights are numeric
        if not (num_rooms.isdigit() and num_beds.isdigit() and num_nights.isdigit()):
            print("Number of rooms, beds, and nights should be numeric.")
            return

        # Check if customer_name is a string and contains at least 3 letters
        if not (isinstance(customer_name, str) and len(customer_name) >= 3 and customer_name.isalpha()):
            print("Customer name should be a string with at least 3 letters.")
            return

        # Convert to integers after confirming they're not empty
        num_rooms = int(num_rooms)
        num_beds = int(num_beds)
        num_nights = int(num_nights)

        # Perform booking and save data to DB
        self.bookingInstance.add_and_process_booking(
            chosen_city, chosen_room_type, num_rooms, num_beds, customer_name, num_nights)
        self.bookingInstance.save_to_db()


        self.CloseAddBookingPage()

    def CloseAddBookingPage(self):
        self.booking_city_label.grid_forget()
        self.booking_city_combobox.grid_forget()
        self.booking_room_type_label.grid_forget()
        self.booking_room_type_combobox.grid_forget()
        self.booking_rooms_label.grid_forget()
        self.booking_rooms_entry.grid_forget()
        self.booking_beds_label.grid_forget()
        self.booking_beds_entry.grid_forget()
        self.booking_name_label.grid_forget()
        self.booking_name_entry.grid_forget()
        self.booking_nights_label.grid_forget()
        self.booking_nights_entry.grid_forget()
        self.booking_submit_button.grid_forget()
        self.booking_back_button.grid_forget()

        self.InitializeBookingManagementPage()

    def InitializeGetAllBookingsPage(self):
        self.bookingTitle.place_forget()
        self.addbookingButton.place_forget()
        self.getbookingsButton.place_forget()
        self.closebookingsButton.place_forget()

        self.getBookingsTitle = tk.Label(self.master, text = "Bookings")
        self.getBookingsTitle.place(relx = 0.5, rely = 0.1, anchor = 'center')

        self.bookingNameLabel = tk.Label(self.master, text = "User Name: ")
        self.bookingNameLabel.place(relx = 0.225, rely = 0.20, anchor = 'center')
        self.bookingNameEntry = ttk.Entry(self.master)
        self.bookingNameEntry.place(relx = 0.50, rely = 0.20, anchor = 'center')
        self.bookingNameApplyButton = tk.Button(self.master, text="Apply", command=self.GetUserBookings)
        self.bookingNameApplyButton.place(relx = 0.70, rely = 0.20, anchor = 'center')

        self.closeGetAllBookingsButton = tk.Button(self.master, text="Close", command=self.CloseGetAllBookings)
        self.closeGetAllBookingsButton.place(relx = 0.5, rely = 0.70, anchor = 'center')

    def GetUserBookings(self):
        userName = self.bookingNameEntry.get()
        if userName:
            bookings = HotelBookingSystem.GetBookingsByUsername(userName)
            print(bookings)
            if bookings and len(bookings) > 0:
                bookings_window = tk.Toplevel(self.master)
                bookings_window.title(f"{userName}'s bookings")
                bookings_window.geometry('720x405')

                bookingsColumnNames = ('booking_id', 'booking_customer', 'booking_hotel', 'booking_room_type', 'booking_number_of_rooms', 'booking_number_of_nights', 'booking_cost')

                bookingsTable = ttk.Treeview(bookings_window, columns=bookingsColumnNames, show='headings')
                bookingsTable.column("#0", width=0, stretch=tk.NO)
                bookingsTable.column("booking_id", anchor=tk.CENTER, width=80)
                bookingsTable.column("booking_customer", anchor=tk.CENTER, width=80)
                bookingsTable.column("booking_hotel", anchor=tk.CENTER, width=80)
                bookingsTable.column("booking_room_type", anchor=tk.CENTER, width=80)
                bookingsTable.column("booking_number_of_rooms", anchor=tk.CENTER, width=80)
                bookingsTable.column("booking_number_of_nights", anchor=tk.CENTER, width=80) 
                bookingsTable.column("booking_cost", anchor=tk.CENTER, width=80)

                bookingsTable.heading("#0", text="", anchor=tk.CENTER)
                bookingsTable.heading("booking_id", text="Id", anchor=tk.CENTER)
                bookingsTable.heading("booking_customer", text="Customer Name", anchor=tk.CENTER)
                bookingsTable.heading("booking_hotel", text="Hotel", anchor=tk.CENTER)
                bookingsTable.heading("booking_room_type", text="Room Type", anchor=tk.CENTER)
                bookingsTable.heading("booking_number_of_rooms", text="Rooms", anchor=tk.CENTER)
                bookingsTable.heading("booking_number_of_nights", text="Nights", anchor=tk.CENTER)
                bookingsTable.heading("booking_cost", text="Cost", anchor=tk.CENTER)

                for i in range(len(bookings)):
                    bookingsTable.insert(parent='', index='end', iid=i, text='', values=tuple(bookings[i]))

                bookingsTable.place(relx=0.5, rely=0.5, anchor='center')

    def CloseGetAllBookings(self):
        self.getBookingsTitle.place_forget()
        self.bookingNameLabel.place_forget()
        self.bookingNameEntry.place_forget()
        self.bookingNameApplyButton.place_forget()
        self.closeGetAllBookingsButton.place_forget()

        self.InitializeBookingManagementPage()

    # Attraction Management View Methods
    def InitializeAttractionManagementPage(self):
        self.DisableHomePage()
        self.master.geometry("500x350")
        self.attractionTitle = tk.Label(self.master, text = "Attraction Management")
        self.attractionTitle.place(relx = 0.5, rely = 0.1, anchor = 'center')
        self.addAttractionButton = tk.Button(self.master, text="Add Attraction", command=self.InitializeAddAttractionPage)
        self.addAttractionButton.place(relx = 0.5, rely = 0.25, anchor = 'center')
        self.getAllAttractionsButton = tk.Button(self.master, text="Get All Attractions", command=self.InitializeGetAllAttractionsPage)
        self.getAllAttractionsButton.place(relx = 0.5, rely = 0.35, anchor = 'center')
        self.addFeedbackButton = tk.Button(self.master, text="Add Feedback", command=self.InitializeAddFeedbackPage)
        self.addFeedbackButton.place(relx = 0.5, rely = 0.45, anchor = 'center')
        self.AttractionsBackButton = tk.Button(self.master, text="Back", command=self.CloseAttractionManagementPage)
        self.AttractionsBackButton.place(relx = 0.5, rely = 0.85, anchor = 'center')
        
    def CloseAttractionManagementPage(self):
        self.attractionTitle.place_forget()
        self.addAttractionButton.place_forget()
        self.getAllAttractionsButton.place_forget()
        self.addFeedbackButton.place_forget()
        self.AttractionsBackButton.place_forget()
        self.DisplayHomePage()

    def InitializeAddAttractionPage(self):
        self.addAttractionButton.place_forget()
        self.getAllAttractionsButton.place_forget()
        self.addFeedbackButton.place_forget()
        self.AttractionsBackButton.place_forget()

        self.attractionTitle.configure(text="Add Attraction")
        self.nameEntryLabel = tk.Label(self.master, text = "Name")
        self.nameEntryLabel.place(relx = 0.25, rely = 0.25, anchor = 'center')
        self.nameEntry = tk.Entry(self.master)
        self.nameEntry.place(relx = 0.5, rely = 0.25, anchor = 'center')
        self.openingHoursEntryLabel = tk.Label(self.master, text = "Opening Hours")
        self.openingHoursEntryLabel.place(relx = 0.20, rely = 0.35, anchor = 'center')
        self.openingHoursEntry = tk.Entry(self.master)
        self.openingHoursEntry.place(relx = 0.5, rely = 0.35, anchor = 'center')
        self.ticketPriceEntryLabel = tk.Label(self.master, text = "Ticket Price")
        self.ticketPriceEntryLabel.place(relx = 0.22, rely = 0.45, anchor = 'center')
        self.ticketPriceEntry = tk.Entry(self.master)
        self.ticketPriceEntry.place(relx = 0.5, rely = 0.45, anchor = 'center')
        self.capacityLimitEntryLabel = tk.Label(self.master, text = "Capacity")
        self.capacityLimitEntryLabel.place(relx = 0.235, rely = 0.55, anchor = 'center')
        self.capacityLimitEntry = tk.Entry(self.master)
        self.capacityLimitEntry.place(relx = 0.5, rely = 0.55, anchor = 'center')

        self.addAttractionSubmitButton = tk.Button(self.master, text="Submit", command=self.SubmitNewAttraction)
        self.addAttractionSubmitButton.place(relx = 0.5, rely = 0.65, anchor = 'center')
        
        self.AddAttractionsBackButton = tk.Button(self.master, text="Back", command=self.CloseAddAttraction)
        self.AddAttractionsBackButton.place(relx = 0.5, rely = 0.85, anchor = 'center')
        
    def CloseAddAttraction(self):  # Adj
        self.attractionTitle.place_forget()
        self.nameEntryLabel.place_forget()
        self.nameEntry.place_forget()
        self.openingHoursEntryLabel.place_forget()
        self.openingHoursEntry.place_forget()
        self.ticketPriceEntryLabel.place_forget()
        self.ticketPriceEntry.place_forget()
        self.capacityLimitEntryLabel.place_forget()
        self.capacityLimitEntry.place_forget()
        self.addAttractionSubmitButton.place_forget()
        self.AddAttractionsBackButton.place_forget()
        self.InitializeAttractionManagementPage()

    def SubmitNewAttraction(self):
        name = self.nameEntry.get()
        openingHours = self.openingHoursEntry.get()
        ticketPrice = self.ticketPriceEntry.get()
        capacityLimit = self.capacityLimitEntry.get()

        if name and openingHours and ticketPrice and capacityLimit:
            newAttraction = Attraction(name=name, openingHours=openingHours, ticketPrice=ticketPrice, capacityLimit=capacityLimit)
            newAttraction.AddAttraction()

            self.attractionTitle.configure(text="Attraction Management")
            self.nameEntryLabel.place_forget()
            self.nameEntry.place_forget()
            self.openingHoursEntryLabel.place_forget()
            self.openingHoursEntry.place_forget()
            self.ticketPriceEntryLabel.place_forget()
            self.ticketPriceEntry.place_forget()
            self.capacityLimitEntryLabel.place_forget()
            self.capacityLimitEntry.place_forget()
            self.addAttractionSubmitButton.place_forget()
            self.InitializeAttractionManagementPage()
        else:
            print("Fill all fields")

    def InitializeGetAllAttractionsPage(self):
        self.addAttractionButton.place_forget()
        self.getAllAttractionsButton.place_forget()
        self.addFeedbackButton.place_forget()
        self.AttractionsBackButton.place_forget()

        self.master.geometry('720x405')

        sortingOptions = ['Ticket Price', 'Capacity']

        self.attractionSortingLabel = tk.Label(self.master, text = "Sort by: ")
        self.attractionSortingLabel.place(relx = 0.325, rely = 0.20, anchor = 'center')
        self.attractionSortingEntry = ttk.Combobox(self.master, width = 10, state="readonly", values = sortingOptions)
        self.attractionSortingEntry.place(relx = 0.45, rely = 0.20, anchor = 'center')
        self.attractionSortingApplyButton = tk.Button(self.master, text="Apply", command=self.ApplyAttractionSorting)
        self.attractionSortingApplyButton.place(relx = 0.60, rely = 0.20, anchor = 'center')
        self.attractionSortingResetButton = tk.Button(self.master, text="Reset", command=self.ResetAttractionSorting)
        self.attractionSortingResetButton.place(relx = 0.70, rely = 0.20, anchor = 'center')

        attractionColumnNames = ('attraction_id', 'attraction_name', 'attraction_openinghours', 'attraction_ticketprice', 'attraction_capacity', 'attraction_feedback')

        self.attractionTitle.configure(text="View All Attractions")
        self.attractionsTable = ttk.Treeview(self.master, columns=attractionColumnNames, show='headings')
        self.attractionsTable.column("#0", width=0, stretch=tk.NO)
        self.attractionsTable.column("attraction_id", anchor=tk.CENTER, width=40)
        self.attractionsTable.column("attraction_name", anchor=tk.CENTER, width=80)
        self.attractionsTable.column("attraction_openinghours", anchor=tk.CENTER, width=80)
        self.attractionsTable.column("attraction_ticketprice", anchor=tk.CENTER, width=80)
        self.attractionsTable.column("attraction_capacity", anchor=tk.CENTER, width=80)
        self.attractionsTable.column("attraction_feedback", anchor=tk.CENTER, width=280) 

        self.attractionsTable.heading("#0", text="", anchor=tk.CENTER)
        self.attractionsTable.heading("attraction_id", text="Id", anchor=tk.CENTER)
        self.attractionsTable.heading("attraction_name", text="Name", anchor=tk.CENTER)
        self.attractionsTable.heading("attraction_openinghours", text="Opening Hours", anchor=tk.CENTER)
        self.attractionsTable.heading("attraction_ticketprice", text="Ticket Price", anchor=tk.CENTER)
        self.attractionsTable.heading("attraction_capacity", text="Capacity", anchor=tk.CENTER)
        self.attractionsTable.heading("attraction_feedback", text="Feedback", anchor=tk.CENTER)

        attractions = Attraction.GetAllAttractions()
        self.AddAttractionsToAttractionsTable(attractions)

        self.attractionsTable.bind("<ButtonRelease-1>", self.ShowFullFeedback)

        self.attractionsTable.place(relx=0.5, rely=0.5, anchor='center')

        self.getAttractionsBackButton = tk.Button(self.master, text="Back", command=self.CloseGetAllAttractions)
        self.getAttractionsBackButton.place(relx = 0.5, rely = 0.85, anchor = 'center')

    def ShowFullFeedback(self, event):
        item = self.attractionsTable.selection()
        if item:
            feedback = self.attractionsTable.item(item, "values")[-1]  # Get the feedback value
            if feedback:
                # Create a Toplevel window to display the full feedback
                feedback_window = tk.Toplevel(self.master)
                feedback_window.title("Full Feedback")
                tk.Label(feedback_window, text=feedback, padx=10, pady=10).pack()

    def CloseGetAllAttractions(self):
        self.master.geometry("500x350")
        self.attractionTitle.place_forget()
        self.attractionsTable.place_forget()
        self.getAttractionsBackButton.place_forget()
        self.attractionSortingLabel.place_forget()
        self.attractionSortingEntry.place_forget()
        self.attractionSortingApplyButton.place_forget()
        self.attractionSortingResetButton.place_forget()
        self.InitializeAttractionManagementPage()

    def ApplyAttractionSorting(self):
        sortingValue = self.attractionSortingEntry.get()
        if sortingValue:
            self.DeleteAttractionTableRows()
            attractions = Attraction.GetAllAttractions()
            sortedAttractions = Attraction.SortAttractions(attractions, sortingValue)
            self.AddAttractionsToAttractionsTable(sortedAttractions)

    def ResetAttractionSorting(self):
        self.attractionSortingEntry.set("")
        self.DeleteAttractionTableRows()
        attractions = Attraction.GetAllAttractions()
        self.AddAttractionsToAttractionsTable(attractions)

    def AddAttractionsToAttractionsTable(self, attractions):
        for i in range(len(attractions)):
            self.attractionsTable.insert(parent='', index='end', iid=i, text='', values=tuple(attractions[i]))

    def DeleteAttractionTableRows(self):
        for row in self.attractionsTable.get_children():
            self.attractionsTable.delete(row)

    def InitializeAddFeedbackPage(self):
        self.addAttractionButton.place_forget()
        self.getAllAttractionsButton.place_forget()
        self.addFeedbackButton.place_forget()
        self.AttractionsBackButton.place_forget()

        attractionNames = Attraction.GetAllAttractionNames()

        self.attractionTitle.configure(text="Add Feedback")
        self.attractionNameEntryLabel = tk.Label(self.master, text = "Name")
        self.attractionNameEntryLabel.place(relx = 0.25, rely = 0.25, anchor = 'center')
        self.attractionNameEntry = ttk.Combobox(self.master, width = 10, state="readonly", values = attractionNames)
        self.attractionNameEntry.place(relx = 0.5, rely = 0.25, anchor = 'center')

        self.attractionFeedbackEntryLabel = tk.Label(self.master, text = "Feedback")
        self.attractionFeedbackEntryLabel.place(relx = 0.225, rely = 0.35, anchor = 'center')
        self.attractionFeedbackEntry = tk.Entry(self.master)
        self.attractionFeedbackEntry.place(relx = 0.5, rely = 0.35, anchor = 'center')

        self.addAttractionFeedbackSubmitButton = tk.Button(self.master, text="Submit", command=self.SubmitNewAttractionFeedback)
        self.addAttractionFeedbackSubmitButton.place(relx = 0.5, rely = 0.65, anchor = 'center')
        
        self.getfeedbacksBackButton = tk.Button(self.master, text="Back", command=self.CloseFeedback)
        self.getfeedbacksBackButton.place(relx = 0.5, rely = 0.85, anchor = 'center')
        
        
        
    def CloseFeedback(self):
        self.attractionTitle.place_forget()  # Clear or reset title text
        self.attractionNameEntryLabel.place_forget()
        self.attractionNameEntry.place_forget()
        self.attractionFeedbackEntryLabel.place_forget()
        self.attractionFeedbackEntry.place_forget()
        self.addAttractionFeedbackSubmitButton.place_forget()
        self.getfeedbacksBackButton.place_forget()
        self.InitializeAttractionManagementPage()
        

    def SubmitNewAttractionFeedback(self):
        attractionName = self.attractionNameEntry.get()
        attractionFeedback = self.attractionFeedbackEntry.get()

        if attractionName and attractionFeedback:
            if not (isinstance(attractionFeedback, str) and len(attractionFeedback) >= 3 and attractionFeedback.isalpha()):
                print("Feedback should be a string with at least 3 characters.")
                return
            else:
                Attraction.AddFeedback(attractionName=attractionName, feedBack=attractionFeedback)

                # Clear the widgets and go back to the Attraction Management Page
                self.attractionTitle.configure(text="Attraction Management")
                self.attractionNameEntryLabel.place_forget()
                self.attractionNameEntry.place_forget()
                self.attractionFeedbackEntryLabel.place_forget()
                self.attractionFeedbackEntry.place_forget()
                self.addAttractionFeedbackSubmitButton.place_forget()
                self.InitializeAttractionManagementPage()
            
        else:
            print("Fill all fields")
