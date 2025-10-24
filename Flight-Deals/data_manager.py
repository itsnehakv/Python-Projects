import requests
import os
from dotenv import load_dotenv
load_dotenv()

# SHEETY_PRICE_AIRLINE_ENDPOINT = os.environ["SHEETY_URL"]
# SHEETY_USERS_ENDPOINT=os.environ["SHEETY_USERS_ENDPOINT"]

class DataManager:
    def __init__(self):
        self._sheety_price_airline_endpoint=os.environ["SHEETY_URL"]
        self._sheety_users_endpoint=os.environ["SHEETY_USERS_ENDPOINT"]
        self.sheet_prices={}
        self.users_response={}


    def getPrice(self):
        sheety_response=requests.get(url=self._sheety_price_airline_endpoint)
        sheet_json=sheety_response.json()
        self.sheet_prices=sheet_json["prices"]
        return self.sheet_prices

    def update_iataCode(self):
        for i in self.sheet_prices :
            updated_code={
                "price":{
                    "iataCode": i["iataCode"]
                }
            }
            update_response=requests.put(url=f"{self._sheety_price_airline_endpoint}/{i["id"]}",json=updated_code)

            print(update_response.text)

    def get_customer_email(self):
        user_data_response=requests.get(url=self._sheety_users_endpoint)
        self.users_response=user_data_response.json()
        return self.users_response





