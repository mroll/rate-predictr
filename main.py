#!/usr/bin/env python3

import argparse
from datetime import datetime

import peewee as pw

import util
from cost import Cost
from cost_estimate import CostEstimate
from location import Location
from lyft_client import LyftClient

db = pw.SqliteDatabase('lyft.db')
db.connect()

db.create_tables([Cost, Location, CostEstimate])

# TODO: Get these creds from env variables or something
client_id = "7lvg-EnyL7sI"
client_secret = "lzCo20mKvk1doYd58-J9QYlh6vHxzyiv"
lyft = LyftClient(client_id, client_secret)


def add_location(args):
    try:
        Location.create(name=args.name, lat=args.lat, lng=args.lng)
    except pw.IntegrityError:
        print('Location by that name already exists')


def get_cost(args):
    try:
        center = Location.get(Location.name == args.center)
    except pw.DoesNotExist:
        print('Location by the name {} is not known'.format(args.center))
        return

    locations = [util.random_location_in_circle(center, args.radius)
                 for i in range(2*args.samples)]

    trips = zip(*[iter(locations)]*2)

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


parser = argparse.ArgumentParser(description='Lyft API interface')
subparsers = parser.add_subparsers(help='sub-command help')


cost_parser = subparsers.add_parser('get_cost', help='get ride cost estimates')
cost_parser.add_argument('--center', dest='center', type=str,
                         help='center of the circle to search')
cost_parser.add_argument('--radius', dest='radius', type=float,
                         help='radius to search within around the center')
cost_parser.add_argument('samples', type=int,
                         help='number of trips for which to request estimated cost')
cost_parser.set_defaults(func=get_cost)

location_parser = subparsers.add_parser('add_location', help='add a location to the db')
location_parser.add_argument('--lat', dest='lat',
                             help='latitude of the new location')
location_parser.add_argument('--lng', dest='lng',
                             help='longitude of the new location')
location_parser.add_argument('name', help='name of the location')
location_parser.set_defaults(func=add_location)

args = parser.parse_args()

args.func(args)
