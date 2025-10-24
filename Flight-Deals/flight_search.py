import os
import requests
from dotenv import load_dotenv
load_dotenv()

IATA_ENDPOINT="https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT="https://test.api.amadeus.com/v2/shopping/flight-offers"

class FlightSearch:
    def __init__(self):
        self._api_key=os.environ["FLIGHT_API_KEY"]
        self._api_secret=os.environ["FLIGHT_API_SECRET"]
        self._token=self._get_new_token()

    #-----Getting bearer authentication token------(at each run)
    def _get_new_token(self):
        header={
            "content-type":"application/x-www-form-urlencoded"
        }

        body={
            "grant_type":"client_credentials",
            "client_id":self._api_key,
            "client_secret":self._api_secret
        }

        flight_token_response=requests.post(url="https://test.api.amadeus.com/v1/security/oauth2/token",data=body,headers=header)
        print(flight_token_response.json())
        print(f"Your token is {flight_token_response.json()['access_token']}")
        print(f"Your token expires in {flight_token_response.json()['expires_in']} seconds")
        return flight_token_response.json()['access_token']


    #-----GETTING Iata code IF that IATA row value is empty (logic in main.py)-----
    def get_iataCode(self, city_name):
        iata_header={
            "Authorization": f"Bearer {self._token}"
        }
        iata_body={
            "keyword":city_name,
            "max":2,
            "include":"AIRPORTS"
        }
        iata_response=requests.get(url=IATA_ENDPOINT,headers=iata_header,params=iata_body)
        print(f"Status code : {iata_response.status_code}")
        try:
            iataCode=iata_response.json()["data"][0]["iataCode"]
        except KeyError:
            print(f"KeyError: No IATA code exists for {city_name}")
            return "N/A"
        except IndexError:
            print(f"IndexError: No IATA code for {city_name}")
            return "Not Found"
        else:
            return iataCode

    #-----GETTING flight data--------
    def check_for_flights(self, originloc, destloc,departdate, returndate, is_direct=True):
        header={"Authorization": f"Bearer {self._token}"}

        query={
            "originLocationCode": originloc,
            "destinationLocationCode":destloc,
            "departureDate": departdate,
            "returnDate": returndate,
            "adults": 1,
            "currencyCode":"GBP",
            "nonStop": "true" if is_direct else "false",
            "max": 10
        }
        print(f"\n➡️ Searching flights {originloc} -> {destloc}")
        print(f"Departure: {departdate}, Return: {returndate}")
        print("Query params:", query)

        flight_response = requests.get(url=FLIGHT_ENDPOINT, headers=header, params=query)

        if flight_response.status_code != 200:
            print(f"❌ check_for_flights() response code: {flight_response.status_code}")
            print("There was a problem with the flight search.")
            print("Response body:", flight_response.text)
            return None

        print("✅ Flight API call succeeded.")
        return flight_response.json()



