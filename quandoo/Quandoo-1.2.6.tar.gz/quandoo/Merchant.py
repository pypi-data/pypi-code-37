from quandoo.QuandooModel import QuandooModel, QuandooDatetime, urljoin
from quandoo.Reservation import Reservation, NewReservation
from quandoo.Error import PoorResponse, PoorRequest
from quandoo.Customer import Customer
import json
import requests
from datetime import datetime, date


class Merchant(QuandooModel):

    def __init__(self, data, agent):
        self.id = data["id"]
        self.name = data["name"]
        address_vals = [i if i in data["location"]["address"].keys() else "" for i in ['number', 'street', 'city', 'country']]
        address_vals[1] = " ".join(address_vals[:1])
        address_vals = address_vals[1:]
        self.address = ", ".join(address_vals)

        self.agent = agent

        super().__init__(data)

    def get_customers(self):
        request = urljoin(self.agent.url, "merchants", self.id, "customers")
        response = requests.get(request, headers=self.agent.headers)

        if response.status_code == 200:
            return [Customer(i, self.agent) for i in json.loads(response.text)["result"]]

        raise PoorResponse(response.status_code, json.loads(response.text), request)

    def get_reservations(self):
        request = "{}/merchants/{}/reservations".format(self.agent.url, self.id)
        response = requests.get(request, headers=self.agent.headers)

        if response.status_code == 200:
            return [Reservation(i, self.agent) for i in json.loads(response.text)["reservations"]]

        raise PoorResponse(response.status_code, json.loads(response.text), request)

    def get_available_times(self, pax: int, date: date, time: str, duration=4):
        date = date.strftime("%Y-%m-%d")
        from_time = tuple(time.split(":"))
        if int(from_time[1]) % 15 != 0:
            raise PoorRequest(
                -1,
                {
                    "errorType": "Time too precise",
                    "errorMessage": "Time's must be increments of 15 mins"
                },
                time
            )
        to_time = str(int(time.split(":")[0]) + duration), time.split(":")[1]
        payload = "times?agentId={}&capacity={}&fromTime={}%3A{}&toTime={}%3A{}".format(
            self.agent.agent_id, pax, from_time[0], from_time[1], to_time[0], to_time[1])

        request = urljoin(self.agent.url, "merchants", self.id, "availabilities", date, payload)
        response = requests.get(request, headers=self.agent.headers)

        if response.status_code == 200:
            return [QuandooDatetime(i["dateTime"]) for i in json.loads(response.text)["timeSlots"]]

        raise PoorResponse(response.status_code, json.loads(response.text), request)

    def create_reservation(self, customer, pax: int, date: date, time: str, duration=4):
        time = time.split(":")
        if int(time[1]) % 15 != 0:
            raise PoorRequest(
                "-1",
                {
                    "errorType": "time too precise",
                    "errorMessage": "time must be in increments of 15 mins"
                },
                ":".join(time)
            )
        datetime_comb = QuandooDatetime(datetime(date.year, date.month, date.day, int(time[0]), int(time[1]), 0))
        data = {
            "reservation": {
                "merchantId": self.id,
                "capacity": pax,
                "dateTime": datetime_comb.get_q_datetime()
            },
            "customer": customer.to_json(),
            "tracking": {
                "agent": {
                    "id": self.agent.agent_id
                }
            }
        }

        request = urljoin(self.agent.url, "reservations")
        response = requests.put(request, headers=self.agent.headers, json=data)

        if response.status_code == 200:
            return NewReservation(json.loads(response.text), self.agent)

        raise PoorResponse(response.status_code, json.loads(response.text), request)

