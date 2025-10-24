from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import get_cheapest_flight
from notification_manager import NotificationManager
import time
from datetime import datetime, timedelta

datamanage=DataManager()
flightsearch=FlightSearch()
notif_manage=NotificationManager()
sheet_place_data=datamanage.getPrice()


print(sheet_place_data)
ORIGIN_LOCATION="LON"

for i in sheet_place_data :
    if i["iataCode"]=="" and i["city"]!="" :
            i["iataCode"]=flightsearch.get_iataCode(i["city"])
            time.sleep(2)   #slowing down requests...

datamanage.sheet_prices=sheet_place_data
datamanage.update_iataCode()

from_date=datetime.now()+timedelta(days=1)  #TOMORROW
to_date=from_date+timedelta(days=(6*30))  #6 MONTHS FROM TOMORROW

from_date=from_date.date()
to_date=to_date.date()


for dest in sheet_place_data:
    flight_data=flightsearch.check_for_flights(
        originloc=ORIGIN_LOCATION,
        destloc=dest["iataCode"],
        departdate=from_date,
        returndate=to_date
    )

    cheapest_flight=get_cheapest_flight(data=flight_data)
    print(f"{dest['city']}: £{cheapest_flight.price}")
    # Slowing down requests to avoid rate limit
    time.sleep(2)

    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {dest['city']}. Looking for indirect flights...")
        stopover_flights = flightsearch.check_for_flights(
            originloc=ORIGIN_LOCATION,
            destloc=dest["iataCode"],
            departdate=from_date,
            returndate=to_date,
            is_direct=False
        )
        cheapest_flight = get_cheapest_flight(stopover_flights)
        print(f"Cheapest indirect flight price is: £{cheapest_flight.price}")

    # if cheapest_flight.price<dest["lowestPrice"] and cheapest_flight.price!="N/A":
        # notif_manage=notif_manage.send_message(price=cheapest_flight.price,
        #                                        depart_code=cheapest_flight.origin,depart_date=cheapest_flight.from_date,
        #                                        arrival_code=cheapest_flight.dest, arrival_date=cheapest_flight.to_date)


    customer_data=datamanage.get_customer_email()
    customer_email_list=[row["whatIsYourEmail?"] for row in customer_data]

    if cheapest_flight.price != "N/A" and cheapest_flight.price < dest["lowestPrice"]:
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct " \
                      f"from {cheapest_flight.origin} to {cheapest_flight.dest}, " \
                      f"on {cheapest_flight.from_date} until {cheapest_flight.to_date}."
        else:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly " \
                      f"from {cheapest_flight.origin} to {cheapest_flight.dest}, " \
                      f"with {cheapest_flight.stops} stop(s) " \
                      f"departing on {cheapest_flight.from_date} and returning on {cheapest_flight.to_date}."

        print(f"Check your email. Lower price flight found to {dest['city']}!")

        notif_manage.send_message(message=message)
        notif_manage.send_email(customer_email_list, message)






