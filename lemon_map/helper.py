# -*- coding: utf-8 -*-
import functools
import haversine


def distance_human_readable(value, cutoff=950):
    """
    transform a distance given in meters into a human readable format
    """
    if value <= cutoff:
        representation = "{:.0f}m".format(value)
    else:
        representation = "{:.2}km".format(value / 1000.0)
    return representation


@functools.lru_cache(maxsize=256)
def geo_distance(point_a, point_b):
    """
    wrapper around the desired distance calculation to facilitate refactoring
    :param point_a: tuple (lat, lon)
    :param point_b: tuple (lat, lon)
    :return: distance in meters
    """
    distance = haversine.haversine(point_a, point_b, unit=haversine.Unit.METERS)
    return distance
