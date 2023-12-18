from django.contrib.auth import authenticate
from .models import *
from rest_framework import serializers
from django.db.models import Sum ,F

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * email
      * password.
    It will try to authenticate the user with when validated.
    """
    email = serializers.CharField(
        label="email",
        write_only=True
    )
    password = serializers.CharField(
        label="password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong email or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs

class getOrderSerializer(serializers.Serializer):
    id=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    name=serializers.SerializerMethodField()
    number_of_orders=serializers.SerializerMethodField()

    def get_name(self,obj):
        return obj.first_name + " " + obj.last_name

    def get_number_of_orders(self,obj):
        wallet=Order.objects.filter(user__id=obj.id)
        return len(wallet)

class BikeStatsSerializer(serializers.Serializer):
    id=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    revenue=serializers.SerializerMethodField()
    journeyTime=serializers.SerializerMethodField()
    orders=serializers.SerializerMethodField()

    def get_revenue(self,obj):
        order=Order.objects.filter(vehicle__id=obj.id).aggregate(Sum('amount'))
        return order['amount__sum']

    def get_journeyTime(self,obj):
        order=Order.objects.filter(vehicle__id=obj.id).annotate(total_difference=F('end_time')-F('start_time'))
        total=order.aggregate(Sum('total_difference'))
        return total['total_difference__sum']

    def get_orders(self,obj):
        order=Order.objects.filter(vehicle__id=obj.id)
        return len(order)

class HottestLocationSerializer(serializers.Serializer):
    id=serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), required=False, allow_null=True)
    name=serializers.CharField()
    numberOfTimesRented=serializers.SerializerMethodField()
    

    def get_numberOfTimesRented(self,obj):
        order=Order.objects.filter(start_location__id=obj.id)
        return len(order)

class VehicleLocationSerializer(serializers.Serializer):
    id=serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), required=False, allow_null=True)
    type=serializers.CharField()
    battery=serializers.IntegerField()
    is_defective=serializers.BooleanField()
    is_available=serializers.BooleanField()
    assigned_to=serializers.SerializerMethodField()
    location_address=serializers.SerializerMethodField()
    location_name=serializers.SerializerMethodField()
    remarks=serializers.CharField()

    def get_assigned_to(self,obj):
        if obj.assigned_to:
            return obj.assigned_to.id
        else:
            return None
        
    def get_location_address(self,obj):
        return obj.location.address

    def get_location_name(self,obj):
        return obj.location.name