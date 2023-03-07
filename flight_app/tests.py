from django.test import TestCase

from flight_app.models import Flight, Order
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import random

def create_flight(flight_num, origin_country, origin_city, origin_code, destination_country, destination_city, destination_code, origin_dt, destination_dt, total_seats, seats_left, is_cancelled, price):
    return Flight.objects.create(flight_num=flight_num, origin_country=origin_country, origin_city=origin_city, origin_code=origin_code, destination_country=destination_country, destination_city=destination_city, destination_code=destination_code, origin_dt=origin_dt, destination_dt=destination_dt, total_seats=total_seats, seats_left=seats_left, is_cancelled=is_cancelled, price=price)

def create_order(flight, user, num_seats, order_dt):
    return Order.objects.create(flight=flight, user=user, num_seats=num_seats, order_dt=order_dt)

def create_user(username, password, email):
    return User.objects.create_user(username=username, password=password, email=email)

def create_mock_data():
    # create 10 flights
    for i in range(10):
        flight_num = f"AA{i}"
        origin_country = "United States"
        origin_city = "New York"
        origin_code = "JFK"   
        destination_country = "United States"
        destination_city = "Los Angeles"
        destination_code = "LAX"
        origin_dt = timezone.now() + datetime.timedelta(days=random.randint(1, 100))
        destination_dt = origin_dt + datetime.timedelta(hours=random.randint(1, 10))
        total_seats = random.randint(1, 100)
        seats_left = random.randint(0, total_seats)
        is_cancelled = random.choice([True, False])
        price = random.randint(100, 1000)
        create_flight(flight_num, origin_country, origin_city, origin_code, destination_country, destination_city, destination_code, origin_dt, destination_dt, total_seats, seats_left, is_cancelled, price)
