import peewee as pw

db = pw.SqliteDatabase('lyft.db')


class Cost(pw.Model):
    estimated_duration_seconds = pw.IntegerField(null=True)
    estimated_distance_miles = pw.FloatField(null=True)
    price_quote_id = pw.CharField(null=True)
    estimated_cost_cents_max = pw.IntegerField(null=True)
    primetime_percentage = pw.CharField(null=True)
    is_valid_estimate = pw.BooleanField(null=True)
    currency = pw.CharField(null=True)
    cost_token = pw.CharField(null=True)
    estimated_cost_cents_min = pw.IntegerField(null=True)
    display_name = pw.CharField(null=True)
    primetime_confirmation_token = pw.CharField(null=True)
    can_request_ride = pw.BooleanField(null=True)

    class Meta:
        database = db
