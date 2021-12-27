# -*- coding: utf-8 -*-


class MapQuery:
    def __init__(self):
        self.ne_lat=None
        self.ne_lng=None
        self.sw_lat=None
        self.sw_lng=None
        self.user_latitude=None
        self.user_longitude=None
        self.zoom = None
        self._response_raw = None
        self._response_timestamp = None

    def get_response(self, token):
        pass

if __name__ == "__main__":
    mq = MapQuery()
