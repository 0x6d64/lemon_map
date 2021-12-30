# -*- coding: utf-8 -*-


def distance_human_readable(value, cutoff=950):
    """
    transform a distance given in meters into a human readable format
    """
    if value <= cutoff:
        representation = "{:.0f}m".format(value)
    else:
        representation = "{:.2}km".format(value / 1000.0)
    return representation
