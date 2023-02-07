from django.urls import path
from .views import *
from .views import Index

urlpatterns = [
    path('Index_page/',Index.as_view(),name='Index_page'),
    path('Index_page/',Index_page,name='Index_page'),
    path('Profile_page/',Profile_page,name='Profile_page'),
    path('',Signin_page,name='Signin_page'),
    path('Signup_page/',Signup_page,name='Signup_page'),
    path('otp_page/',otp_page,name='otp_page'),
    path('Changepassword_page/',Changepassword_page,name='Changepassword_page'),
    path('Cart_page/',Cart_page,name='Cart_page'),



    # ///****************************************** Functionality *************************************///


    path('Signup/',Signup,name='Signup'),
    path('Signin/',Signin,name='Signin'),
    path('Signout/', Signout, name='Signout'),
    path('Changepassword/', Changepassword, name='Changepassword'),
    # path('verify_otp/<str:verify_for>/', verify_otp, name='verify_otp'),


]