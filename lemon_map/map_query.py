# -*- coding: utf-8 -*-
import datetime
import json

import requests

from api_helper import LIME_API_BASE_URL
from exceptions import LemonQueryException
from vehicles import Scooter, NonScooter
from helper import geo_distance


class MapQuery:
    def __init__(self, query_parameters=None):
        self.user_latitude = None
        self.user_longitude = None
        self.ne_lat = None
        self.ne_lng = None
        self.sw_lat = None
        self.sw_lng = None
        self.zoom = None
        self.response_raw = None
        self.timestamp = None
        if query_parameters:
            if not isinstance(query_parameters, dict):
                raise LemonQueryException("query_parameters must be a dict!")
            self.initialize_from_dict(query_parameters)

    def initialize_from_dict(self, parameter_dict):
        self.ne_lat = parameter_dict.get("ne_lat", self.ne_lat)
        self.ne_lng = parameter_dict.get("ne_lng", self.ne_lng)
        self.sw_lat = parameter_dict.get("sw_lat", self.sw_lat)
        self.sw_lng = parameter_dict.get("sw_lng", self.sw_lng)
        self.user_latitude = parameter_dict.get("user_latitude", self.user_latitude)
        self.user_longitude = parameter_dict.get("user_longitude", self.user_longitude)
        self.zoom = parameter_dict.get("zoom", self.zoom)

    def represent_as_dict(self):
        dict_representation = {
            "user_latitude": self.user_latitude,
            "user_longitude": self.user_latitude,
            "ne_lat": self.ne_lat,
            "ne_lng": self.ne_lng,
            "sw_lat": self.sw_lat,
            "sw_lng": self.sw_lng,
            "zoom": self.zoom,
        }
        return dict_representation

    @classmethod
    def from_config_instance(cls, config_instance):
        new_cls = cls()
        parameters = {
            "user_latitude": config_instance.get("MAP", "user_lat"),
            "user_longitude": config_instance.get("MAP", "user_lon"),
            "ne_lat": config_instance.get("MAP", "northlimit"),
            "ne_lng": config_instance.get("MAP", "eastlimit"),
            "sw_lat": config_instance.get("MAP", "southlimit"),
            "sw_lng": config_instance.get("MAP", "westlimit"),
            "zoom": config_instance.get("MAP", "zoom"),
        }
        new_cls.initialize_from_dict(parameters)
        return new_cls

    def request_map_view(self, token):
        api_request = requests.get(
            LIME_API_BASE_URL + "/rider/v1/views/map",
            data=self.represent_as_dict(),
            headers={"authorization": "Bearer {}".format(token)},
        )
        if not api_request.ok:
            raise LemonQueryException(
                "error requesting vehicles: Response {}, {}".format(
                    api_request.status_code, api_request.content
                )
            )
        self.timestamp = datetime.datetime.now()
        self.response_raw = json.loads(api_request.content)


class MapViewParser:
    def __init__(self, user_lat=None, user_lon=None):
        self.user_lat = user_lat
        self.user_lon = user_lon

    def parse_map_view(self, mapview_data, timestamp=None):
        parsed_vehicles = set()
        if not timestamp:
            timestamp = datetime.datetime.now()
        attributes_to_extract = [
            "plate_number",
            "latitude",
            "longitude",
            "battery_percentage",
            "operating_status",
            "type_name",
        ]
        data = mapview_data.get("data")
        bikes_data = data.get("attributes").get("bikes")
        for vehicle in bikes_data:
            vehicle_data = {"id": vehicle.get("id")}
            for item in attributes_to_extract:
                vehicle_data[item] = vehicle.get("attributes").get(item)
            if vehicle_data.get("type_name") == "scooter":
                new_vehicle = Scooter(attribute_dict=vehicle_data, timestamp=timestamp)
            else:
                new_vehicle = NonScooter(attribute_dict=vehicle_data, timestamp=timestamp)
            parsed_vehicles.add(new_vehicle)
        if self.user_lat and self.user_lon:
            self._update_straightline_distances(parsed_vehicles)
        return parsed_vehicles

    def parse_file(self, filename):
        with open(filename) as fp:
            data = json.load(fp)
            timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
            parsed_data = self.parse_map_view(data, timestamp=timestamp)
        return parsed_data

    def _update_straightline_distances(self, vehicles):
        user_location = (self.user_lat, self.user_lon)
        for v in vehicles:
            v_location = (v.latitude, v.longitude)
            distance = geo_distance(v_location, user_location)
            v.distance_straight = distance


if __name__ == "__main__":
    import config
    import auth
    import os

    lemon_config = config.LemonConfig().from_file("../.lemon_config.ini")
    auth_file = os.path.join("..", lemon_config.get("DEFAULT", "auth_file"))
    my_auth = auth.LemonAuth().from_token_file(auth_file)

    example_json = "../data_raw/example_response3.json"
    parser = MapViewParser(user_lat=45.79919616985226, user_lon=24.155758121471834)
    vehicles = parser.parse_file(example_json)
    for x in sorted(vehicles, key=lambda x: x.distance_straight):
        print(str(x))

    print("done")
