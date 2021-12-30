# -*- coding: utf-8 -*-
import datetime


class Vehicle:
    def __init__(self, attribute_dict=None):
        self.id = None
        self._process_attribute_dict(attribute_dict)

    def _process_attribute_dict(self, attribute_dict):
        assert isinstance(attribute_dict, dict)
        for attribute_name in attribute_dict:
            self.__setattr__("_" + attribute_name, attribute_dict.get(attribute_name))

    @property
    def plate_number(self):
        return self._plate_number

    @property
    def type(self):
        return self._type_name

    @property
    def soc(self):
        return self._battery_percentage

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def in_service(self):
        return self._operating_status == "in_service"

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        str_representation = "{type}|{plate}@{soc}%|{lat}|{lon}".format(
            type=self.type,
            plate=self.plate_number,
            soc=self.soc,
            lat=self.latitude,
            lon=self.longitude,
        )
        return str_representation


class Scooter(Vehicle):
    pass


class NonScooter(Vehicle):
    pass


class VehicleStats:
    def __init__(self):
        # TODO
        pass
