from pprint import pprint
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import *

data = DataManager()
sheet_data = data.get_destination_data()
# print(sheet_data)


for each in sheet_data:
    if each["iataCode"] == "":
        iata_update = FlightSearch(each["city"]).find_iata_code()
        each["iataCode"] = iata_update

        data.destination_data = sheet_data
        data.update_iata_codes()

ORIGIN_CITY_IATA = "PNQ"
flight_search = FlightSearch(city=ORIGIN_CITY_IATA)
notification_manager = NotificationManager()


tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        flight_search.city,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flight.price < destination["lowestPrice"]:
        notification_manager.send_sms(
            message=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        )
