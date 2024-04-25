import pandas as pd
import threading
import time
import tkinter as tk
from tkinter import ttk
import sqlite3

from Utilities.DBUtilities import *

class SimpleQueue:
    def __init__(self):
        self._queue = []
        self._lock = threading.Lock()
        self._task_done = threading.Event()

    def put(self, item):
        with self._lock:
            self._queue.append(item)
            self._task_done.clear() 

    def get(self):
        with self._lock:
            if self._queue:
                return self._queue.pop(0)
            else:
                return None

    def task_done(self):
        self._task_done.set()  

    def join(self):
        self._task_done.wait(0.5)  
    
    
class HotelBookingSystem:
    def __init__(self):
        self.hotels_data = self.load_hotels_data()
        self.reservation_processor = ReservationProcessor(self.hotels_data)

    def load_hotels_data(self):
        hotels_data = pd.read_csv('hotels1_data.csv')
        return hotels_data

    def run(self):
        chosen_city, chosen_room_type, num_rooms, num_beds = self.get_user_choices()

        filtered_hotels = self.filter_hotels(chosen_city, chosen_room_type, num_beds)

        if filtered_hotels.empty:
            print("No matching hotels found.")
        else:
            user_preferences = self.get_user_preferences(chosen_room_type, num_beds)

            sorted_hotels = self.sort_hotels_by_distance(filtered_hotels, user_preferences)
            print("\nRecommended Hotels:")
            self.print_hotels(sorted_hotels)

            choice = self.get_user_hotel_choice(sorted_hotels)

            chosen_hotel = sorted_hotels.iloc[choice - 1]
            print(f"\nBooking request for {chosen_hotel['name']}")
            customer_name, num_nights = self.get_booking_details()

            total_cost = self.calculate_total_cost(chosen_hotel, num_nights, num_rooms, chosen_room_type)

            self.reservation_processor.add_booking_request(
                customer_name, chosen_hotel['name'], chosen_room_type, num_rooms, num_nights, total_cost
            )

        
            self.reservation_processor.add_sentinel()  # Add sentinel value to signal the end of booking requests
            self.reservation_processor.wait_for_bookings()

            print("Booking request sent for processing.")

            # Generate reports
            self.reservation_processor.generate_booking_report()

    def get_user_choices(self):
        chosen_city = self.get_city_choice()
        chosen_room_type, num_rooms, num_beds = self.get_room_choice()
        return chosen_city, chosen_room_type, num_rooms, num_beds

    def get_city_choice(self):
        print("Cities:")
        cities = self.hotels_data['location'].unique()
        for i, city in enumerate(cities, start=1):
            print(f"{i}. {city}")
        while True:
            try:
                city_index = int(input("Enter the number of the city: ")) - 1
                chosen_city = cities[city_index] if 0 <= city_index < len(cities) else None
                if chosen_city is not None:
                    return chosen_city
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def get_room_choice(self):
        room_types = {
            'Standard': 'Standard',
            'Deluxe': 'Deluxe',
            'Executive_Suite': 'Executive_Suite',
            'Single': 'Single',
            'Double': 'Double',
            'Family_Suite': 'Family_Suite',
            'Triple': 'Triple',
        }

        print("\nRoom Types:")
        for i, room_type in enumerate(room_types, start=1):
            print(f"{i}. {room_type}")

        while True:
            try:
                room_index = int(input("Enter the number of the room type: ")) - 1
                chosen_room_type = list(room_types.values())[room_index] if 0 <= room_index < len(room_types) else None

                if chosen_room_type:
                    num_rooms = int(input(f"Enter the number of rooms for {chosen_room_type}: "))
                    num_beds = int(input(f"Enter the number of beds for {chosen_room_type}: "))
                    return chosen_room_type, num_rooms, num_beds
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def filter_hotels(self, city, room_type, num_beds):
        filtered_hotels = self.hotels_data[
            (pd.notna(self.hotels_data['location'])) &  # Filter out NaN values
            (self.hotels_data['location'] == city) &
            (self.hotels_data[room_type + '_rooms'] > 0) &
            (self.hotels_data[room_type + '_beds'] >= num_beds)
        ]
        return filtered_hotels

    def get_user_preferences(self, chosen_room_type, num_beds):
        user_preferences = {
            'rating': float(input("Enter your preferred rating: ")),
            'chosen_room_type': chosen_room_type,
            'num_beds': num_beds
        }
        return user_preferences

    def sort_hotels_by_distance(self, filtered_hotels, user_preferences):
        filtered_hotels['distance'] = filtered_hotels.apply(
            lambda x: self.calculate_distance(x, user_preferences), axis=1
        )
        sorted_hotels = filtered_hotels.sort_values(by='distance')
        return sorted_hotels

    def calculate_distance(self, hotel, user_preferences):
        distance = ((hotel['rating'] - user_preferences['rating']) ** 2 +
                    (hotel[f'{user_preferences["chosen_room_type"]}_beds'] - user_preferences['num_beds']) ** 2) ** 0.5
        return distance

    def calculate_total_cost(self, chosen_hotel, num_nights, num_rooms, chosen_room_type):
        room_type = chosen_hotel['name'].replace(' ', '_')  
        price_column = f'{chosen_room_type}_price'
        chosen_hotel_dict = chosen_hotel.to_dict()
        
        price_per_night = int(chosen_hotel_dict[price_column])  
        return price_per_night * num_nights * num_rooms

    def print_hotels(self, hotels):
        for i, (index, hotel) in enumerate(hotels.iterrows(), start=1):
            print(f"{i}. {hotel['name']} - Rating: {hotel['rating']}")

    def get_user_hotel_choice(self, hotels):
        while True:
            try:
                choice = int(input("Enter the number of your chosen hotel: "))
                if 1 <= choice <= len(hotels):
                    return choice
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def get_booking_details(self):
         while True:
            try:
                customer_name = input("Enter your name: ")
                if not customer_name.replace(" ", "").isalpha():
                    raise ValueError("Invalid input. The name must contain only alphabetic characters.")

                num_nights = int(input("Enter the number of nights: "))
                return customer_name, num_nights
            except ValueError as ve:
                print(str(ve))

    def add_and_process_booking(self, chosen_city, chosen_room_type, num_rooms, num_beds, customer_name, num_nights):
        filtered_hotels = self.filter_hotels(chosen_city, chosen_room_type, num_beds)

        if filtered_hotels.empty:
            print("No matching hotels found.")
        else:
            user_preferences = {'rating': 4.0, 'chosen_room_type': chosen_room_type, 'num_beds': num_beds}

            sorted_hotels = self.sort_hotels_by_distance(filtered_hotels, user_preferences)

            print("\nRecommended Hotels:")
            self.print_hotels(sorted_hotels)

            choice = 1  # For simplicity, automatically choose the first hotel

            chosen_hotel = sorted_hotels.iloc[choice - 1]
            print(f"\nBooking request for {chosen_hotel['name']}")
            total_cost = self.calculate_total_cost(chosen_hotel, num_nights, num_rooms, chosen_room_type)

            self.reservation_processor.add_booking_request(
                customer_name, chosen_hotel['name'], chosen_room_type, num_rooms, num_nights, total_cost
            )

            self.reservation_processor.wait_for_bookings()
            print("Booking request sent for processing.")

    def save_to_csv(self):
        booking_data = pd.DataFrame(self.reservation_processor.bookings)
        print(booking_data)
        booking_data.to_csv('bookings_data.csv', index=False)
        print("Booking data saved to 'bookings_data.csv'.")

    def save_to_db(self):
        booking_data = self.reservation_processor.bookings
        connection = DBUtils.InitializeDB()
        cursor = connection.cursor()
        try:
            for row in booking_data:
                cursor.execute('''
                INSERT INTO booking 
                (booking_customer, booking_hotel, booking_room_type, booking_number_of_rooms, booking_number_of_nights, booking_cost) 
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (row["customer_name"], 
                    row["hotel_name"], 
                    row["room_type"], 
                    row["num_rooms"],
                    row["num_nights"],
                    row["total_cost"]))
            connection.commit()
        except Exception as e:
            print(f"Error adding booking to db")
        connection.close() 
        
    def GetBookingsByUsername(name):
        connection = DBUtils.InitializeDB()
        cursor = connection.cursor()
        rows = []
        try:
            cursor.execute('''
            SELECT * FROM booking
            WHERE booking_customer = ?
            ''', (name,)
            )

            rows = cursor.fetchall()
            connection.commit()
        except Exception as e:
            print(f"Error")
        connection.close() 
        return rows
        
class ReservationProcessor:
    def __init__(self, hotels_data):
        self.booking_queue = SimpleQueue()
        self.hotels_data = hotels_data
        self.bookings = [] 
        self.thread = threading.Thread(target=self.process_bookings)
        self.thread.start()

    def add_sentinel(self):
        # Add a sentinel value to indicate the end of booking requests
        self.booking_queue.put(None)

    def add_booking_request(self, customer_name, hotel_name, room_type, num_rooms, num_nights, total_cost):
        booking_request = {
            'customer_name': customer_name,
            'hotel_name': hotel_name,
            'room_type': room_type,
            'num_rooms': num_rooms,
            'num_nights': num_nights,
            'total_cost': total_cost
        }
        self.booking_queue.put(booking_request)
        self.process_bookings()

    def process_bookings(self):
        while True:
            booking_request = self.booking_queue.get()
            if booking_request:
                self.process_booking2(booking_request)
            else:
                break

    def process_booking2(self, booking_request):
        time.sleep(1)  
        print(f"Booking processed for {booking_request['customer_name']} - "
              f"Hotel: {booking_request['hotel_name']}, Room Type: {booking_request['room_type']}, "
              f"Total Cost: {booking_request['total_cost']}")
        self.bookings.append(booking_request)  

    def wait_for_bookings(self):
        self.booking_queue.join()

    def generate_booking_report(self):
        print("\nBooking Report:")
        print("Customer Name | Hotel Name | Room Type | Nights | Total Cost")
        print("------------------------------------------------------------")
        for booking in self.bookings:
            print(f"{booking['customer_name']} | {booking['hotel_name']} | "
                  f"{booking['room_type']} | {booking['num_nights']} | "
                  f"{booking['total_cost']}")
            
            

if __name__ == "__main__":
    # Instantiate HotelBookingSystem and run the GUI
    hotel_booking_system = HotelBookingSystem()
    hotel_booking_system.run()
