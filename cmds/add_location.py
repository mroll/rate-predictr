import peewee as pw

from models.location import Location


def add_location(args):
    try:
        Location.create(name=args.name, lat=args.lat, lng=args.lng)
    except pw.IntegrityError:
        print('Location by that name already exists')
