class FlightData:
    def __init__(self, origin, dest, from_date,to_date, price, stops):
        self.origin=origin
        self.dest=dest
        self.from_date=from_date
        self.to_date=to_date
        self.price=price
        self.stops=stops

def get_cheapest_flight(data):
    # print(data)
    if data is None or not data["data"]:     #not data["data"]----> if "data" (list) isn't present is data variable/object
        print("There is no flight data")
        return FlightData("N/A","N/A","N/A","N/A","N/A","N/A") #for the 5 arguements initialized


    first_flight_data=data["data"][0]
    lowest_price=float(first_flight_data["price"]["grandTotal"])
    no_of_stops = len(first_flight_data["itineraries"][0]["segments"]) - 1
    depart_code=first_flight_data["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    depart_date=first_flight_data["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    if len(first_flight_data["itineraries"]) == 1:
        arrival_code = first_flight_data["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
        arrival_date =first_flight_data["itineraries"][0]["segments"][-1]["arrival"]["at"].split("T")[0]
    else:
    # Final destination is found in the last segment of the flight
        arrival_code=first_flight_data["itineraries"][0]["segments"][no_of_stops]["arrival"]["iataCode"]
    # Return date is taken as the arrival date of the final segment in the return itinerary
        arrival_date=first_flight_data["itineraries"][1]["segments"][-1]["arrival"]["at"].split("T")[0]

    cheapest_flight=FlightData(price=lowest_price, origin=depart_code, dest=arrival_code,
                               from_date=depart_date,to_date=arrival_date, stops=no_of_stops)

    for info in data["data"]:
        price=float(info["price"]["grandTotal"])
        if price<lowest_price:
            lowest_price=price
            depart_code = info["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            depart_date = info["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            if len(first_flight_data["itineraries"]) == 1:
                arrival_code = info["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
                arrival_date = info["itineraries"][0]["segments"][-1]["arrival"]["at"].split("T")[0]
            else:
                # Final destination is found in the last segment of the flight
                arrival_code = info["itineraries"][0]["segments"][no_of_stops]["arrival"]["iataCode"]
                # Return date is taken as the arrival date of the final segment in the return itinerary
                arrival_date = info["itineraries"][1]["segments"][-1]["arrival"]["at"].split("T")[0]
            cheapest_flight = FlightData(price=lowest_price, origin=depart_code, dest=arrival_code,
                                         from_date=depart_date, to_date=arrival_date)
            print(f"Lowest price to {depart_code} is £{lowest_price}")

    return cheapest_flight







