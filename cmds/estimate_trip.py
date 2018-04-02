import math
import textwrap
import peewee as pw

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

    return (dx * dx + dy * dy) < radius * radius


def similar_trips(start, end, radius, n=0):
    radius = float(radius)

    similar_start_locations = (CostEstimate.select()
            .join(
                Location,
                on=(CostEstimate.start_location == Location.id)
            )
            .join(Cost, on=(CostEstimate.cost == Cost.id))
            .where(
                point_in_circle(
                    CostEstimate.start_location,
                    start,
                    radius
                )
            ))

    similar_estimates = []

    for estimate in similar_start_locations:
        if point_in_circle(estimate.end_location, end, radius):
            similar_estimates.append(estimate.cost)

    if n == 0:
        return similar_estimates
    else:
        return similar_estimates[:n]


def estimate_trip(args):
    try:
        start = Location.get(Location.name == args.start)
        end = Location.get(Location.name == args.end)
    except pw.DoesNotExist:
        print("Start or End Location is not known.")
        return
    
    previous_estimates = similar_trips(start, end, args.radius)

    if previous_estimates:
        avg_cost_max = 0
        avg_cost_min = 0

        for cost in previous_estimates:
            avg_cost_max += cost.estimated_cost_cents_max
            avg_cost_min += cost.estimated_cost_cents_min

        avg_cost_max = (avg_cost_max / len(previous_estimates)) / 100
        avg_cost_min = (avg_cost_min / len(previous_estimates)) / 100

        print("Estimated cost of trip from {} to {}: (${}, ${})".format(
            start.name, end.name, avg_cost_min, avg_cost_max))
        print("Number of estimates aggregated: {}".format(
            len(previous_estimates)))
    else:
        print(textwrap.dedent("""
                No simliar trips found from {} to {}
                with location precision of {} miles.
            """.format(
            start.name, end.name, args.radius)))
