# -*- coding: utf-8 -*-


class Vehicle:
    def __init__(self, attribute_dict=None):
        self.id = None
        self._process_attribute_dict(attribute_dict)

    def _process_attribute_dict(self, attribute_dict):
        # TODO: finish
        pass

    def __hash__(self):
        return hash(self.id)


class Scooter(Vehicle):
    pass


class NonScooter(Vehicle):
    pass


class VehicleStats:
    def __init__(self):
        # TODO
        pass
