import peewee as pw

from models.cost import Cost
from models.location import Location

db = pw.SqliteDatabase('lyft.db')


class CostEstimate(pw.Model):
    cost = pw.ForeignKeyField(Cost, backref='cost_estimates')
    start_location = pw.ForeignKeyField(Location, backref='cost_estimates')
    end_location = pw.ForeignKeyField(Location, backref='cost_estimates')
    time = pw.DateTimeField()

    class Meta:
        database = db
