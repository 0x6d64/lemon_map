# lemon_map

A scraper for Lime scooter data.

## Usage

Start with the ``--help`` parameter to get usage help.

## Config file

The following code block shows an example of a config file:

```ini
[DEFAULT]
auth_file = ./lemon_auth.json
[MAP]
user_lat = 46.79919616985226
user_lon = 25.155758121471834
northlimit = 46.8010909742
eastlimit = 25.157554211
southlimit = 46.7969706826
westlimit = 25.153627457
zoom = 16
```

The parameters ``user_lat`` and ``user_lon`` give the latitude or longitude that shall be assumed as the user location (
for calculation of distances).

The ``<xx>limit`` parameters define the bounding box around the user that shall be queried. The ``zoom``
parameter is not fully understood, but according to
[the api reference](
https://github.com/ubahnverleih/WoBike/blob/master/Lime.md#get-vehicles-and-zones)
zoom levels of <15 lead to the clustering of bikes
(this is probably a bad thing for us).

## Resources

* API reference:
  https://github.com/ubahnverleih/WoBike/blob/master/Lime.md
* Bounding box definition:
  https://boundingbox.klokantech.com/

