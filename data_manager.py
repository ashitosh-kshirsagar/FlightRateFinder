from pprint import pprint

import requests


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get("SHEETY_API").json()
        self.destination_data = response
        return self.destination_data["prices"]

    def update_iata_codes(self):
        for each in self.destination_data:
            new_code = {
                "price": {
                    "iataCode": each["iataCode"]
                }

            }
            update_code = requests.put(f"{'SHEETY_API'}/{each['id']}", json=new_code)
            print(update_code.text)
