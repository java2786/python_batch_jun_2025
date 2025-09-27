# Ticket booking system

from threading import Thread
import time

# total_available_tickets = 5
train = 12345

def book_train_ticket(passenger_name, train_number):
    print(f"Starting ticket booking for {passenger_name} on train {train_number}")
    time.sleep(1/2)

    print(f"Ticket is booked successfully for {passenger_name} on train {train_number}")
 
    # if(total_available_tickets>0):
        # print(f"Ticket is booked successfully for {passenger_name} on train {train_number}")
        # # total_available_tickets -= 1
    # else:
    #     print(f"All tickets are sold on train {train_number}")

passengers = ["Ramesh", "Suresh", "Mahesh", "Mukesh", "Ganesh", "Dinesh", "Rithesh", "Hitesh"]

for passenger in passengers:
    passenger_thread = Thread(target=book_train_ticket, args=(passenger, train))
    passenger_thread.start()
    passenger_thread.join()
    
print("All bookings are complete")