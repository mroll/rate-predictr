import random
from datetime import datetime

import peewee as pw

import util
from lyft_client import LyftClient
from models.cost import Cost
from models.cost_estimate import CostEstimate
from models.location import Location

client_id, client_secret = util.load_credentials()
lyft = LyftClient(client_id, client_secret)


# in miles
MIN_TRIP_DIST = .7
MAX_TRIP_DIST = 30


def trip(center, radius, trip_distance):
    start = util.random_location_in_circle(center, radius)
    end = util.random_location_in_circle(start, trip_distance)

    return (start, end)


def trip_distance_sampler(low, high):
    def sampler():
        nonlocal low, high
        return random.uniform(low, high)

    return sampler


def get_costs(args):
    global lyft, MIN_TRIP_DIST, MAX_TRIP_DIST

    try:
        center = Location.get(Location.name == args.center)
    except pw.DoesNotExist:
        print('Location by the name {} is not known'.format(args.center))
        return

    sample_trip_distance = trip_distance_sampler(MIN_TRIP_DIST, MAX_TRIP_DIST)

    trips = [trip(center, args.radius, sample_trip_distance()) for i in range(args.samples)]

    for start, end in trips:
        cost_json = lyft.get_cost(
            ride_type='lyft',
            **start.as_start(),
            **end.as_end()
        )
        cost = Cost.create(**cost_json.__dict__['__data__'])
        start = Location.create(**start.__dict__['__data__'])
        end = Location.create(**end.__dict__['__data__'])

        CostEstimate.create(
            cost=cost,
            start_location=start,
            end_location=end,
            time=datetime.now()
        )
