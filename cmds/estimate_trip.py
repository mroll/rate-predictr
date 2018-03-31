import math
import random

from models.location import Location
from models.cost import Cost
from models.cost_estimate import CostEstimate

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


def point_in_circle(point, center, radius):
    dx = (center.lat - point.lat) / miles_to_lat
    dy = (center.lng - point.lng) / miles_to_lng

    return math.sqrt(math.pow(dx,2) + math.pow(dy,2)) < radius


def distance(p1, p2):
    dx = (p1.lat - p2.lat) / miles_to_lat
    dy = (p1.lng - p2.lng) / miles_to_lng

    return hypotenuse(dx, dy)

def hypotenuse(x, y):
    return math.sqrt(math.pow(x,2) + math.pow(y,2))


def similar_trips(start, end, radius, n=0):
    estimates = (CostEstimate
            .select()
            .where(
                point_in_circle(
                    CostEstimate.start_location,
                    start,
                    radius
                ) and
                point_in_circle(
                    CostEstimate.end_location,
                    end,
                    radius
                )
            ))

    if n == 0:
        return estimates
    else:
        #return estimates.sort(key=normalize_distances)[:n]
        return estimates[:n]


def estimate_trip(args):
    try:
        start = Location.get(Location.name == args.start)
        end = Location.get(Location.name == args.end)
    except pw.DoesNotExist:
        print("Start or End Location is not known.")
        return
    print(util.similar_trips(start, end, args.radius))

