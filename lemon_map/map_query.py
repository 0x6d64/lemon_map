# -*- coding: utf-8 -*-
import datetime
import json

import requests

from api_helper import LIME_API_BASE_URL
from exceptions import LemonQueryException
from vehicles import Scooter, NonScooter


class MapQuery:
    def __init__(self, query_parameters=None):
        self.user_latitude = None
        self.user_longitude = None
        self.ne_lat = None
        self.ne_lng = None
        self.sw_lat = None
        self.sw_lng = None
        self.zoom = None
        self._response_raw = None
        self._response_timestamp = None
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
        self._response_timestamp = datetime.datetime.now()
        self._response_raw = json.loads(api_request.content)


class MapViewParser:
    def __init__(self):
        self._vehicles = set()
        pass

    def parse_map_view(self, mapview_data):
        """
        TODO
        quick outline on what to do:
        iterate over data first pass, create instance of Scooter for each scooter found
        then do a second pass where we complete the data from the second part of the dict
        validate that we don't have a mismatch between first and second pass
        the scooters need to have the ID assigned to each other
        """
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
                new_vehicle = Scooter(vehicle_data)
            else:
                new_vehicle = NonScooter(vehicle_data)
            self._vehicles.add(new_vehicle)

    def parse_file(self, filename):
        with open(filename) as fp:
            data = json.load(fp)
            self.parse_map_view(data)


if __name__ == "__main__":
    import config
    import auth
    import os

    lemon_config = config.LemonConfig().from_file("../.lemon_config.ini")
    auth_file = os.path.join("..", lemon_config.get("DEFAULT", "auth_file"))
    my_auth = auth.LemonAuth().from_token_file(auth_file)

    example_json = "../data_raw/example_response3.json"
    parser = MapViewParser()
    parser.parse_file(example_json)
    print(parser._vehicles)
