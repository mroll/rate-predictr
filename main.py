#!/usr/bin/env python3

import argparse

import peewee as pw

import util
from cmds import add_location, get_costs
from models.cost import Cost
from models.cost_estimate import CostEstimate
from models.location import Location

db = pw.SqliteDatabase('lyft.db')
db.connect()

db.create_tables([Cost, Location, CostEstimate])

parser = argparse.ArgumentParser(description='Lyft API interface')
subparsers = parser.add_subparsers(help='sub-command help')


cost_parser = subparsers.add_parser('get_costs',
                                    help='get ride cost estimates')
cost_parser.add_argument('--center', dest='center', type=str,
                         help='center of the circle to search')
cost_parser.add_argument('--radius', dest='radius', type=float,
                         help='radius to search within around the center')
cost_parser.add_argument('samples', type=int,
                         help='number of trips for which to request estimated cost')
cost_parser.set_defaults(func=get_costs)

location_parser = subparsers.add_parser('add_location',
                                        help='add a location to the db')
location_parser.add_argument('--lat', dest='lat',
                             help='latitude of the new location')
location_parser.add_argument('--lng', dest='lng',
                             help='longitude of the new location')
location_parser.add_argument('name', help='name of the location')
location_parser.set_defaults(func=add_location)

args = parser.parse_args()

args.func(args)
