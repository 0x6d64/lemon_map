# -*- coding: utf-8 -*-
import functools
import haversine
import matplotlib.pyplot as pplot


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


def plot_vehicles(vehicles, user_coordinates=None, circle_radius=1000, show=True):
    """

    :param vehicles:
    :param user_coordinates:
    :param circle_radius:
    :return:
    """

    longitudes = list()
    latitudes = list()
    for veh in vehicles:
        latitudes.append(veh.latitude)
        longitudes.append(veh.longitude)

    fig, axes = pplot.subplots()
    axes.set_box_aspect(1.0)
    axes.scatter(longitudes, latitudes, marker=".")

    if user_coordinates:
        user_lat, user_lon = user_coordinates
        axes.scatter(user_lon, user_lat, marker=".")

        if circle_radius:
            circle_lat, circle_lon = haversine.inverse_haversine(
                (user_lat, user_lon), circle_radius, 0, unit=haversine.Unit.METERS
            )
            radius_for_plot = circle_lat - user_lat
            circle = pplot.Circle((user_lon, user_lat), radius_for_plot, alpha=0.25)
            axes.add_patch(circle)
    if show:
        pplot.show()

    return axes
