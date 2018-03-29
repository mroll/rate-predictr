import peewee as pw

db = pw.SqliteDatabase('lyft.db')


class Location(pw.Model):
    lat = pw.FloatField()
    lng = pw.FloatField()
    name = pw.CharField(unique=True, null=True)

    class Meta:
        database = db

    def as_start(self):
        return {'start_lat': self.lat, 'start_lng': self.lng}

    def as_end(self):
        return {'end_lat': self.lat, 'end_lng': self.lng}
