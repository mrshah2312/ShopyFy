from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from random import randint
from django.views import View




def Index_page(request):
    return render(request,'index.html')

def Profile_page(request):
    return render(request,'profile.html')

def Signin_page(request):
    return render(request,'signin.html')

def Signup_page(request):
    return render(request,'signup.html')

def otp_page(request):
    return render(request,'otp.html')

def Changepassword_page(request):
    return render(request, "changepassword.html")

def Cart_page(request):
    return render(request, "cart.html")




# ///****************************************** Functionality *************************************///

# Signup Functionality
def Signup(request):
    if request.POST['password'] == request.POST['cpassword']:
        try:
            Master.objects.get(Email=request.POST['email'])
            messages.error(request, "User Already Exist.")
            return render(request,'signup.html')

        except Master.DoesNotExist:
            master = Master.objects.create(Email=request.POST['email'],Password=request.POST['password'])
            Customers.objects.create(Master=master)
            messages.success(request, "User Sign Up Successfully.")
            return redirect(Signin_page)
            # return render(request,'index.html')

    else:
        messages.error(request, "Both Password Should Be Same.")
        return redirect(Signup_page)

        
# Signin Functionality
def Signin(request):
    try:
        master = Master.objects.get(Email = request.POST['email'])
        if master.Password == request.POST['password']:
            request.session['email'] = master.Email
            messages.success(request, "Welcome to GrossyFy.")
            return redirect(Index_page)
        else:
            messages.success(request, "Password Does Not Match.")
            return render(request,"signin.html")
        
    except Master.DoesNotExist:
        messages.error(request, "User Does Not Exist.")
        return render(request,"signin.html")

# Signout Functionality
def Signout(request):
    if 'email' in request.session:
        del request.session['email']
        messages.success(request, "User Sign Out Successfully.")
        return redirect(Signin_page)
    return redirect(Index_page)


# OTP Creation
def otp(request):
    otp_number = randint(1000, 9999)
    print("OTP is: ", otp_number)
    request.session['otp'] = otp_number

# send_otp
def send_otp(request, otp_for="register"):
    print(otp_for)
    otp(request)

    email_to_list = [request.session['reg_data']['email'],]

    if otp_for == 'activate':
        request.session['otp_for'] = 'activate'
        subject = f'OTP for Budget Account Activation'
    elif otp_for == 'recover_pwd':
        request.session['otp_for'] = 'recover_pwd'
        subject = f'OTP for Budget Password Recovery'
    else:
        request.session['otp_for'] = 'register'
        subject = f'OTP for Budget Registration'

    email_from = settings.EMAIL_HOST_USER

    message = f"Your One Time Password for verification is: {request.session['otp']}."

    send_mail(subject, message, email_from, email_to_list)


# verify otp
def verify_otp(request, verify_for="register"):

    if request.session['otp'] == int(request.POST['otp']):
        if verify_for == 'activate':
            master = Master.objects.get(Email=request.session['reg_data']['email'])
            # master.Password = request.session['reg_data']['password']
            master.IsActive = True
            master.save()
            return redirect(profile_page)
        elif verify_for == 'recover_pwd':
            master = Master.objects.get(Email=request.session['reg_data']['email'])
            master.Password = request.session['reg_data']['password']
            master.save()
        else:
            print('before new account')
            master = Master.objects.create(
                Email = request.session['reg_data']['email'],
                Password = request.session['reg_data']['password'],
                IsActive = True,
            )
            UserProfile.objects.create(
                Master = master,
            )
            print('after new account')
        print("verified.")
        del request.session['reg_data']

    else:
        print("Invalid OTP")
        return redirect(otp_page)
    return redirect(Signin_page)

# Change Password Functionlity
def Changepassword(request):
    master = Master.objects.get(Email=request.session['email'])
    if master.Password == request.POST['current_password']:
        if request.POST['new_password'] == request.POST['confirm_password']:
            master.Password = request.POST['new_password']
            master.save()
            messages.success(request, "Password Changed Successfully.")
            return redirect(Changepassword_page)
        else:
            messages.error(request, "New Password and Confirm Password Does Not Match.")
            return redirect(Changepassword_page)
    else:
        messages.error(request, "Password and Current Password Does Not Match.")
        return redirect(Changepassword_page)


# # register view
# def signup(request):
#     try:
#         masters = Master.objects.all()
#         for master in masters:
#             if request.POST['email'] == master.Email:
#                 raise IntegrityError

#         password = request.POST['password']
#         if password == request.POST['confirm_password']:
#             request.session['reg_data'] = {
#                 'email': request.POST['email'],
#                 'password': password,
#             }

#             send_otp(request)

#             print('OTP sent successfully.')

#             return redirect(otp_page)
#         else:
#             print('both password should be same.')

#     except IntegrityError as err:
#         print(err)
#         print('email already exist. please login.')
    
#         return redirect(Signin_page)

#     return redirect(Signup_page)

class Index(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect(Index_page)

    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()

        data = {}
        data['products'] = products
        data['categories'] = categories

        if 'email' in request.session:
            # profile_data(request) # load profile data
            return render(request, 'index.html',data)
        else:
            return redirect(Signin_page)