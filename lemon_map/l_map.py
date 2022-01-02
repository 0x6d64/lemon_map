# -*- coding: utf-8 -*-
import logging
from exceptions import LemonException, LemonQueryException, LemonAuthException
from map_query import MapViewParser
from vehicle_stats import VehicleStats

logger = logging.getLogger(__name__)


class LemonMap:
    def __init__(self):
        self.query = None
        self.vehicles = None
        self.token = None
        self.timestamp = None
        self.vehicle_stats = None

    def execute_query_and_parse_data(self):
        try:
            self.query.request_map_view(self.token)
        except LemonQueryException as ex:
            logger.error("got error during query: {}".format(ex))
            raise ex
        self.timestamp = self.query.timestamp
        parser = MapViewParser(
            user_lat=self.query.user_latitude, user_lon=self.query.user_longitude
        )
        self.vehicles = parser.parse_map_view(self.query.response_raw, timestamp=self.timestamp)
        self.vehicle_stats = VehicleStats(self.vehicles)
