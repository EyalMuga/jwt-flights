from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db.models import Subquery, OuterRef
import flight_app
from django.db.models import Q


class Flight(models.Model):
    flight_num = models.CharField(
        db_column="flight_num", null=False, blank=False, max_length=24
    )
    origin_country = models.CharField(
        db_column="origin_country", null=False, blank=False, max_length=128
    )
    origin_city = models.CharField(
        db_column="origin_city", null=False, blank=False, max_length=128
    )
    origin_code = models.CharField(
        db_column="origin_code", null=False, blank=False, max_length=24
    )
    destination_country = models.CharField(
        db_column="destination_country", null=False, blank=False, max_length=128
    )
    destination_city = models.CharField(
        db_column="destination_city", null=False, blank=False, max_length=128
    )
    destination_code = models.CharField(
        db_column="destination_code", null=False, blank=False, max_length=24
    )
    origin_dt = models.DateTimeField(
        db_column="origin_dt", null=False, blank=False
    )
    destination_dt = models.DateTimeField(
        db_column="destination_dt", null=False, blank=False
    )
    total_seats = models.IntegerField(
        db_column="total_seats",
        null=False,
        blank=False,
        validators=[MinValueValidator(0)],
    )
    seats_left = models.IntegerField(
        db_column="seats_left",
        null=False,
        blank=False,
        validators=[MinValueValidator(0)])

    is_cancelled = models.BooleanField(db_column="is_cancelled", default=False)
    price = models.FloatField(db_column="price", null=False, blank=False)



    def __str__(self) -> str:
        return (
            f"Flight number: {self.flight_num} from {self.origin_country}-{self.origin_city} to {self.destination_country}-{self.destination_city}"
            f" for {self.price} EUR with {self.seats_left} seats left"
        )

    def save(self, *args, **kwargs):
        # if seats left is not set, set it to total seats
        if not self.seats_left:
            self.seats_left = self.total_seats
        super().save(*args, **kwargs)

    class Meta:
        db_table = "flights"


class Order(models.Model):
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)
    seats = models.IntegerField(db_column="seats", null=False, blank=False)
    order_date = models.DateField(
        db_column="order_date", auto_now=True, null=True, blank=True
    )
    total_price = models.FloatField(
        db_column="total_price", null=True, blank=True)

    class Meta:
        db_table = "orders"

    def clean(self) -> ValidationError | None:
        if self.seats > self.flight.seats_left:
            raise ValidationError(
                {
                    "seats": "There are not enough seats left on this flight."
                }
            )

    # update seats left after saving
    def save(self, *args, **kwargs):
        self.total_price = self.flight.price * self.seats
        self.flight.seats_left -= self.seats
        super().save(*args, **kwargs)
        self.flight.save()
