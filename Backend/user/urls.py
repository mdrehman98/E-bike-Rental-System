from django.urls import path
from . import views

urlpatterns = [

    path("registerUser",views.UserAPI.as_view(),name="registerUser"),
    path("getCustomerDetails",views.getUserDetails.as_view()),
    path("ForgotPassword",views.ForgotPass.as_view()),
    path("updateCustomerDetails/<int:pk>/",views.UserAPI.as_view(),name='updateCustomerDetails'),
    path("deleteCustomerDetails/<str:pk>/",views.UserAPI.as_view()),
    path("LoginUser",views.LoginView.as_view()),
    path("createLocation",views.LocationAPI.as_view(),name="createLocation"),
    path("deleteLocation",views.LocationAPI.as_view()),
    path("getLocationDetails",views.LocationAPI.as_view(),name='getLocationDetails'),
    path("createVehicle",views.VehicleAPI.as_view()),
    path("getVehicleDetails",views.VehicleAPI.as_view()),
    path("updateVehicleDetails",views.VehicleAPI.as_view()),
    path("deleteVehicleDetails",views.VehicleAPI.as_view()),
    path("getBikesPerLocation/<str:pk>/",views.Rent.as_view(),name='getBikesPerLocation'),
    path("AssignBike",views.Rent.as_view()),
    path("getBikesAssignedPerUser",views.Return.as_view()),
    path("ReturnBike",views.Return.as_view()),
    path("ReportBike",views.Report.as_view()),
    path("OperatorOperationsOnVehicle",views.OperatorVehicleActions.as_view()),
    path("ShowBalance",views.PayAnyCharges.as_view()),
    path("RechargeWallet",views.Recharge.as_view()),
    path("PerBikeStats",views.PerBikeStats.as_view()),
    path("HottestLocation",views.HottestLocation.as_view()),
    path("TotalStats",views.TotalStats.as_view()),
    path("OrderPerUser",views.getTotalOrders.as_view())
]