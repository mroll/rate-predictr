import math
import os
import random
import sys
import textwrap

from models.location import Location

lat_to_lat_distance = 69    # miles
lng_to_lng_distance = 53    # miles

miles_to_lat = 1 / lat_to_lat_distance
miles_to_lng = 1 / lng_to_lng_distance


def random_point_in_circle(center, radius):
    theta = random.random()*2*math.pi
    r = random.random()*radius

    px, py = (r*math.cos(theta), r*math.sin(theta))

    return (center.lat + px * miles_to_lat, center.lng + py * miles_to_lng)


def random_location_in_circle(center, radius):
    p = random_point_in_circle(center, radius)
    return Location(lat=p[0], lng=p[1])


def fread(fname):
    with open(fname, 'r') as fp:
        return fp.read()


def load_credentials():
    client_id = os.environ.get('LYFT_CLIENT_ID')
    client_secret = os.environ.get('LYFT_CLIENT_SECRET')

    if client_id is None or client_secret is None:
        error_message = textwrap.dedent("""
            Error loading Lyft Credentials.
            Set credentials as environment variables:
                LYFT_CLIENT_ID
                LYFT_CLIENT_SECRET
            or consider adding to your shell profile script.
            """)
        print(error_message)
        sys.exit(1)
    else:
        return client_id, client_secret
