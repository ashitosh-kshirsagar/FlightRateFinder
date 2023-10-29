from pprint import pprint
from flight_data import Flightdata
import requests


class FlightSearch:
    def __init__(self, city):
        self.city = city
        self.iata_code = ""

    def find_iata_code(self):
        TEQUILA_API = "https://api.tequila.kiwi.com/locations/query"
        headers = {"apikey": "TEQUILA API KEY"}
        parameters = {"term": self.city, "location_types": "city"}
        response = requests.get(TEQUILA_API, params=parameters, headers=headers).json()
        self.iata_code = response["locations"][0]["code"]
        return self.iata_code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": "TEQUILA API KEY"}
        flight_check_parameters = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "INR"
        }

        response = requests.get(url=f"https://api.tequila.kiwi.com/v2/search", params=flight_check_parameters,
                                headers=headers)

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = Flightdata(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: Rs.{flight_data.price}")
        return flight_data
