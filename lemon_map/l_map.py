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


if __name__ == "__main__":
    import config
    import auth
    import os
    import timeit

    lemon_config = config.LemonConfig().from_file("../.lemon_config.ini")
    auth_file = os.path.join("..", lemon_config.get("DEFAULT", "auth_file"))
    my_auth = auth.LemonAuth().from_token_file(auth_file)

    example_json = "../data_raw/example_response3.json"
    parser = MapViewParser(user_lat=45.79919616985226, user_lon=24.155758121471834)

    iterations = 100
    tt = timeit.timeit(lambda: parser.parse_file(example_json), number=iterations)

    vehicles = parser.parse_file(example_json)
    for x in sorted(vehicles, key=lambda x: x.distance_straight):
        print(str(x))

    print("{} iterations took {:.3f}ms".format(iterations, tt * 1000))
    print("done")
