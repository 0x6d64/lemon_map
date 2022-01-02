# -*- coding: utf-8 -*-
import statistics

from helper import geo_distance


class VehicleStats:
    def __init__(self, vehicles, user_coordinates=None):
        self.vehicles = vehicles
        self._sort_vehicles()
        self.user_coordinates = user_coordinates
        self._distances_to_user = [x.distance_straight for x in self.vehicles]

    def _sort_vehicles(self):
        self.vehicles = sorted(self.vehicles, key=lambda x: x.distance_straight)

    @property
    def nearest_scooter(self):
        return self.vehicles[0]

    @property
    def median_distance(self):
        return statistics.median(self._distances_to_user)

    @property
    def mean_distance(self):
        return statistics.mean(self._distances_to_user)
