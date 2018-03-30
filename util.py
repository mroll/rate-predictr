import math
import random
import os
import sys

from location import Location

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

def load_credentials():
    cred_filename = "token.txt"
    client_id = os.environ.get('LYFT_CLIENT_ID')
    client_secret = os.environ.get('LYFT_CLIENT_SECRET')

    if client_id == None or client_secret == None:
        creds_found = [False, False]
        try:
            with open(cred_filename) as lyft_creds_file:
                for line in lyft_creds_file:
                    if line.split("=")[0] == 'LYFT_CLIENT_ID':
                        client_id = line.split("=")[1]
                        creds_found[0] = True
                    elif line.split("=")[0] == 'LYFT_CLIENT_SECRET':
                        client_secret = line.split("=")[1]
                        creds_found[1] = True
        except IOError as error:
            print("\nError Loading Lyft Credentials!")
            print("Set as Environment Variables or", \
                    f"declare in '{cred_filename}'\n")
            sys.exit(1)

        if not all(cred == True for cred in creds_found):
            print("\nError: Lyft Credentials", \
                    f"in '{cred_filename}' are invalid\n")
            sys.exit(1)
    return client_id, client_secret
