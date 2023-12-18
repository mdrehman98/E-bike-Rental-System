import datetime
from django.shortcuts import render
from uuid import uuid4
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import *
from django.conf import settings
from django.forms import model_to_dict
from rest_framework_jwt.utils import jwt_encode_handler
from . import serializers
import datetime
from datetime import timezone
from django.db.models import Sum ,F , Count
import jwt 
# Create your views here.


class CustomResponse():
    def successResponse(self, data, status=status.HTTP_200_OK, description="SUCCESS"):
        return Response(
            {
                "success": True,
                "error_code": 0,
                "description": description,
                "info": data
            }, status=status
        )

    def errorResponse(self, data={}, description="ERROR", errorCode=1, status=status.HTTP_400_BAD_REQUEST):
        return Response(
            {
                "success": False,
                "errorCode": errorCode,
                "description": description,
                "info": data
            }, status=status
        )


def jwt_payload_handler(user):
    payload = {
        'exp': datetime.datetime.utcnow() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA'],
        'user_id': user.id,
        'email': user.email,
    }

    return payload


def createJWTtoken(user, description):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    response = {"user_id": str(user.id), "token": token,
                "description": description, "type": user.user_type}
    return CustomResponse().successResponse(data=response)


class UserAPI(APIView):
    permission_classes = [AllowAny, ]

    @transaction.atomic
    def post(self, request):
        first_name = request.data['first_name']
        last_name = request.data.get('last_name', None)
        email = request.data['email']
        password = request.data['password']
        type = request.data['type']
        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.user_type = type
        user.set_password(password)
        user.save()
        Wallet.objects.create(balance=100, amount_spent=0, user=user)
        return createJWTtoken(user, description="Created User and token for user")
        # return CustomResponse().successResponse(description="User details saved",data=[])

    @transaction.atomic
    def put(self, request, pk):
        first_name = request.data['first_name']
        last_name = request.data.get('last_name', None)
        email = request.data['email']
        password = request.data['password']
        type = request.data['type']
        user_list = User.objects.filter(id=pk).first()
        if user_list:
            user_list.first_name = first_name
            user_list.last_name = last_name
            user_list.email = email
            user_list.user_type = type
            user_list.set_password(password)
            user_list.save()
            return CustomResponse().successResponse(description="details of user have been update", data=[])
        return CustomResponse().errorResponse(description="invalid user id")

    def delete(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if user:
            user.delete()
            wallet = Wallet.objects.filter(user=user)
            wallet.delete()
            return CustomResponse().successResponse(description="user details with given id to deleted", data=[])
        else:
            return CustomResponse().errorResponse(description="error detecting user details", data=[])

class getUserDetails(APIView):

    permission_classes = (AllowAny,)
    def post(self, request):
        user_id = request.data.get('user_id', None)
        if user_id:
            user_list = User.objects.filter(id=user_id)
        else:
            user_list = User.objects.all()
        if user_list:
            return CustomResponse().successResponse(description="User details are", data=user_list.values())
        else:
            return CustomResponse().errorResponse(description="invalid user id/ error in inputs")


class LoginView(TokenObtainPairView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        email=request.data['email']
        password=request.data['password']
        user=User.objects.get(email=email)
        if user is None:
            return Response(description="no user found",data=[],status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            return Response(description="password does not match",data=[],status=status.HTTP_400_BAD_REQUEST)
        response = super().post(request, format)
        #if response.status_code == status.HTTP_200_OK:
            # Token obtained successfully, add additional data to the response
        #    user = User.objects.get(email=request.data['email'])
        #    response.data['user_id'] = user.id
        #    response.data['email'] = user.email

        return response

        #return Response(data=response_data, status=status.HTTP_200_OK)
        #return createJWTtoken(user, description="Logged in User and token for user")


class ForgotPass(APIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        email = request.data['email']
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']

        user = User.objects.filter(email=email).first()
        if user is None:
            return CustomResponse().errorResponse(description="No user with the given email", data=[])
        if new_password != confirm_password:
            return CustomResponse().errorResponse(description="Passwords Do not match", data=[])

        user.set_password(new_password)
        user.save()
        return CustomResponse().successResponse(description="New Password has been set", data=[])


class LocationAPI(APIView):

    @transaction.atomic
    def post(self, request):
        name = request.data['name']
        address = request.data['address']
        # total_bikes=request.data['total_bikes']
        location = Location.objects.create(name=name, address=address)
        if location:
            return CustomResponse().successResponse(description="location details created", data=[])
        else:
            return CustomResponse().errorResponse(description="error creating location", data=[])

    #renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        location_id = request.data.get('id', None)
        if location_id:
            location = Location.objects.filter(id=location_id)
        else:
            location = Location.objects.all()
        context={"location":location}
        if location:
            return Response(context, template_name='index.html')
            #return CustomResponse().successResponse(description="location details", data=location.values())
        else:
            return CustomResponse().errorResponse(description="error fetching location")

    def delete(self, request):
        location_id = request.data['location_id']
        location = Location.objects.filter(id=location_id)
        location.delete()
        return CustomResponse().successResponse(description="location deleted", data=[])


class VehicleAPI(APIView):
    permission_classes = [AllowAny, ]

    @transaction.atomic
    def post(self, request):
        type = request.data['type']
        location_id = request.data['location_id']
        location = Location.objects.filter(id=location_id).first()
        vehicle = Vehicle.objects.create(type=type, location=location)
        location.total_bikes += 1
        location.save()
        return CustomResponse().successResponse(description="Vehicle details created", data=[])

    def get(self, request):
        vehicle_id = request.data.get('vehicle_id', None)
        if vehicle_id:
            vehicle = Vehicle.objects.filter(id=vehicle_id)
        else:
            vehicle = Vehicle.objects.all()
        if vehicle:
            serializer=serializers.VehicleLocationSerializer(vehicle,many=True)
            return CustomResponse().successResponse(description="Vehicle details are", data=serializer.data)
        else:
            return CustomResponse().errorResponse(description="invalid vehicle id/ error in inputs")

    def put(self, request, pk):
        type = request.data['type']
        location = request.data['location']
        vehicle = Vehicle.objects.filter(
            id=pk).update(type=type, location=location)
        if vehicle:
            return CustomResponse().successResponse(description="Vehicle details updated", data=[])
        return CustomResponse().errorResponse(description="invalid vehicle id")

    def delete(self, request, pk):
        vehicle = Vehicle.objects.filter(id=pk).first()
        location = Location.objects.filter(id=vehicle.location.id).first()
        location.total_bikes -= 1
        location.save()
        if vehicle:
            vehicle.delete()
            return CustomResponse().successResponse(description="vehicle details with given id to deleted", data=[])
        else:
            return CustomResponse().errorResponse(description="error detecting vehicle details", data=[])

# @transaction.atomic


class Rent(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, pk):

        vehicle = Vehicle.objects.filter(
            location=pk, is_defective=False, is_available=True)
        if vehicle:
            return CustomResponse().successResponse(description="vehicle in given location id", data=vehicle.values())
        else:
            return CustomResponse().errorResponse(description="error detecting vehicle details", data=[])

    @transaction.atomic
    def post(self, request):
        vehicle_id = request.data['vehicle_id']
        user_id = request.data['user_id']
        user = Vehicle.objects.filter(assigned_to__id=user_id)
        print(user)
        if user.exists():
            return CustomResponse().errorResponse(description="A vehicle is already assigned to the user", data=[])
        wallet=Wallet.objects.filter(user__id=user_id).first()
        if wallet.balance<=0:
            return CustomResponse().errorResponse(description="Balance insuffient, please recharge", data=model_to_dict(wallet))
        
        user = User.objects.filter(id=user_id).first()
        vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        if vehicle.battery<=0:
            return CustomResponse().errorResponse(description="Battery Too Low,Please Select another Vehicle", data=[])
        # wallet=Wallet.objects.filter(user__id=user_id).first()
        vehicle.assigned_to = user
        vehicle.is_available = False
        location = Location.objects.filter(id=vehicle.location.id).first()
        location.total_bikes -= 1
        location.save()
        vehicle.save()
        order = Order.objects.create(start_location=location, start_time=datetime.datetime.now(
            timezone.utc), user=user, vehicle=vehicle)
        # if vehicle.save():
        return CustomResponse().successResponse(description="vehicle assigned to user", data=model_to_dict(vehicle))


class Return(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        user_id = request.data['user_id']
        # location_id=request.data['location_id']
        user = User.objects.filter(id=user_id).first()
        # location=Location.objects.filter(id=location_id).first()
        vehicle = Vehicle.objects.filter(assigned_to=user)
        if vehicle:
            return CustomResponse().successResponse(description="vehicle details assigned to user", data=vehicle.values())
        else:
            return CustomResponse().errorResponse(description="no vehicle assigned to user", data=[])

    # ASK FRONT END ABOUT ORDER ID AND UPDATE ORDER ID
    @transaction.atomic
    def post(self, request):
        user_id = request.data['user_id']
        location_id = request.data['location_id']
        location = Location.objects.filter(id=location_id).first()
        vehicle = Vehicle.objects.filter(assigned_to__id=user_id).first()
        if not vehicle:
            return CustomResponse().errorResponse(description="No vehicle to return", data=[])
        wallet = Wallet.objects.filter(user__id=user_id).first()
        order = Order.objects.filter(user__id=user_id, active=True).first()
        hours_used = float((datetime.datetime.now(
            timezone.utc) - order.start_time).total_seconds() / 3600)
        if vehicle.type == 'electric_scooter':
            min_amount = 10
        else:
            min_amount = 15
        total_amount_to_be_deducted = (hours_used) * min_amount
        wallet.balance = float(wallet.balance)-total_amount_to_be_deducted
        wallet.amount_spent = float(
            wallet.amount_spent)+total_amount_to_be_deducted
        order.active = False
        order.amount = total_amount_to_be_deducted
        order.end_time = datetime.datetime.now(timezone.utc)
        order.end_location = location
        vehicle.assigned_to = None
        vehicle.is_available = True
        vehicle.battery -= 20
        vehicle.location = location
        # location=vehicle.location
        location.total_bikes += 1
        wallet.save()
        order.save()
        location.save()
        vehicle.save()
        return CustomResponse().successResponse(description="vehicle returned successfully", data=model_to_dict(wallet))


class Report(APIView):
    permission_classes = [AllowAny, ]

    @transaction.atomic
    def post(self, request):
        vehicle_id = request.data['vehicle_id']
        remarks = request.data.get("remarks", None)
        vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        location = Location.objects.filter(id=vehicle.location.id).first()
        location.total_bikes -= 1
        vehicle.is_defective = True
        vehicle.remarks = remarks
        vehicle.save()
        location.save()
        return CustomResponse().successResponse(description="vehicle reported defective successfully", data=[])


class OperatorVehicleActions(APIView):
    permission_classes = [AllowAny, ]

    @transaction.atomic
    def post(self, request):
        vehicle_id = request.data['vehicle_id']
        action = request.data['action']
        location_to_move = request.data.get("location_id", None)
        vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        if action == 'charge':
            vehicle.battery = 100
        elif action == 'repair':
            vehicle.is_defective = False
            location = Location.objects.filter(id=vehicle.location.id).first()
            location.total_bikes += 1
            location.save()
        elif action == 'move_vehicle':
            location = Location.objects.filter(id=vehicle.location.id).first()
            location.total_bikes -= 1
            location.save()
            new_location = Location.objects.filter(id=location_to_move).first()
            vehicle.location = new_location
            new_location.total_bikes += 1
            new_location.save()
        vehicle.save()
        if vehicle:
            return CustomResponse().successResponse(description="vehicle operation done successfully", data=[])
        else:
            return CustomResponse().errorResponse(description="no vehicle with this id", data=[])


class Recharge(APIView):
    permission_classes = [AllowAny, ]

    @transaction.atomic
    def post(self, request):
        user_id = request.data['user_id']
        amount = request.data['amount']
        wallet = Wallet.objects.filter(user__id=user_id).first()
        wallet.balance += amount
        wallet.save()
        return CustomResponse().successResponse(description="Wallet has been recharged", data=[])


class PayAnyCharges(APIView):
    permission_classes = [AllowAny, ]

    @transaction.atomic
    def post(self, request):
        user_id = request.data['user_id']
        wallet = Wallet.objects.filter(user__id=user_id, is_active=True).first()
        return CustomResponse().successResponse(description="Amount to be payed", data=model_to_dict(wallet))

class getTotalOrders(APIView):
    permission_classes = [AllowAny, ]

    def post(self,request):
        user=User.objects.all()
        serializer=serializers.getOrderSerializer(user,many=True)

        return CustomResponse().successResponse(description="order per user is", data=serializer.data)

class PerBikeStats(APIView):
    permission_classes = [AllowAny, ]

    def post(self,request):
        vehicle=Vehicle.objects.all()
        serializer=serializers.BikeStatsSerializer(vehicle,many=True)

        return CustomResponse().successResponse(description="stats per bike is", data=serializer.data)

class HottestLocation(APIView):
    permission_classes = [AllowAny, ]

    def post(self,request):
        location=Location.objects.all()
        serializer=serializers.HottestLocationSerializer(location,many=True)

        return CustomResponse().successResponse(description="hottest location is", data=serializer.data)

class TotalStats(APIView):
    permission_classes = [AllowAny, ]

    def post(self,request):
        amt=Order.objects.aggregate(Sum('amount'))
        number=Order.objects.all().distinct('vehicle_id')
        order=Order.objects.all()
        response={"Total_Amount":amt['amount__sum'],"Total_Bikes_rented":len(number),"Total_Orders":len(order)}
        return CustomResponse().successResponse(description="All time Stats", data=response)

