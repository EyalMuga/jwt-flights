from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from datetime import datetime
from .models import Flight, Order

# register serializer for user creation and login (token)
class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "confirm_password",
            "email",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "password": {"write-only": True},
            "confirm_password": {"write-only": True},
        }
    # validate password and confirm password fields
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Password fields don't match."}
            )

        try:
            validate_password(attrs["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"password": e})

        return attrs

    # create user and save to database
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

# user serializer for user profile view and update (token)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "is_staff",
        ]

# flight serializer for flight list view (token) and flight detail view (token) and flight create view (token)
class FlightSerializer(serializers.ModelSerializer):
    origin_time = serializers.SerializerMethodField()
    destination_time = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        exclude = [
            "origin_dt",  # = origin_time
            "destination_dt",  # = destination_time
        ]
    # format datetime fields
    def get_origin_time(self, obj):
        return datetime.strftime(obj.origin_dt, "%d/%m/%Y %H:%M:%S")
    # format datetime fields
    def get_destination_time(self, obj):
        return datetime.strftime(obj.destination_dt, "%d/%m/%Y %H:%M:%S")

# order serializer for order list view (token) and order detail view (token) and order create view (token)
class OrderSerializer(serializers.ModelSerializer):
    date_submitted = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    flight_num = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = [
            "order_date",  # = date_submitted
        ]

# format datetime fields
    def get_date_submitted(self, obj):
        return datetime.strptime(f"{obj.order_date}", "%Y-%m-%d").strftime("%d-%m-%Y")
    
# use user id to get user name
    def get_user_name(self, obj):
        user = User.objects.get(pk=obj.user.id)
        return user.first_name + " " + user.last_name
    
# flight id to get flight number
    def get_flight_num(self, obj):
        flight = Flight.objects.get(pk=obj.flight.id)
        return flight.flight_num