import math

from models.location import Location
from models.cost import Cost
from models.cost_estimate import CostEstimate

lat_to_lat_distance = 69    # miles
lng_to_lng_distance = 53    # miles

miles_to_lat = 1 / lat_to_lat_distance
miles_to_lng = 1 / lng_to_lng_distance


def point_in_circle(point, center, radius):
    dx = (center.lat - point.lat) / miles_to_lat
    dy = (center.lng - point.lng) / miles_to_lng

    return hypotenuse(dx, dy) < radius


def distance(p1, p2):
    dx = (p1.lat - p2.lat) / miles_to_lat
    dy = (p1.lng - p2.lng) / miles_to_lng

    return hypotenuse(dx, dy)

def hypotenuse(x, y):
    return math.sqrt(math.pow(x,2) + math.pow(y,2))


def similar_trips(start, end, radius, n=0):
    estimates = (CostEstimate
            .select(CostEstimate, Location)
            .join(
                Location, on=(CostEstimate.start_location == Location)
            )
            .join(
                Location, on=(CostEstimate.end_location == Location)
            )
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
    print(similar_trips(start, end, args.radius))

