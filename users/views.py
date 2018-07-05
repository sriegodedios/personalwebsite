from django.shortcuts import render
from django.contrib.auth import login, authenticate, update_session_auth_hash
#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.forms import SignUpForm, LoginForm, AddressForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from users.models import ContactInformation, Profile
from django.db.models import Q


# Create your views here.
def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request)
            return redirect('../profile/address-info')
    else:
        form = SignUpForm()
    return render(request, 'users/registration.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=raw_password)
            login(request, user)
            return redirect('main')
        else:
            messages.success(request, 'Incorrect username and/or password combination.')

    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required(login_url='/users/login/')
def index(request):
    fname = request.user.first_name
    lname = request.user.last_name
    st = "%s %s" %(fname,lname)
    return render(request, 'users/index.html', {'username': st, 'location':'Dashboard', 'logout':'../users/logout'})

def ajax(request):
    return render(request, 'users/pages/404.html')

@login_required(login_url='/users/login/')
def ResetPassword(request):
    fname = request.user.first_name
    lname = request.user.last_name
    st = "%s %s" %(fname,lname)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('../change-password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change-password.html', {
        'form': form, 'username': st, 'location': 'Profile / Password Reset', 'logout':'../../logout'
    })

@login_required(login_url='/users/login/')
def AddressPage(request):
    location = "Profile / Address"
    fname = request.user.first_name
    lname = request.user.last_name
    st = "%s %s" %(fname,lname)

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request,"Address Saved!")
            print("working")
            return redirect('../../profile')
        else:
            messages.error(request, "The form wasn't valid for some reason")
            #return redirect('../address-info')
            #print(get_object_or_404(form))
            print("Not working")

    else:
        form = AddressForm()
    return render(request, 'users/update-address.html', {
        'form': form, 'username': st, 'location': location, 'logout':'../../logout'
    })

def AddressChange(request):
    location = "Profile / Address / Change"

    if request.method == "Post":
        query = ContactInformation.objects.filter(username = request.user.username)

        if not query:
            return render(request, 'users/profile.html', {'username': st, 'user': request.user, 'location': 'Profile', 'logout':'../logout', 'form': form})





@login_required(login_url='/users/login/')
def profile(request):
    location = "Profile"
    form = PasswordChangeForm(request.user)
    args = {'form': form}
    fname = request.user.first_name
    lname = request.user.last_name
    st = "%s %s" %(fname,lname)
    #print(request.user.username)
    query = ContactInformation.objects.filter(username = request.user.username)

    if not query:
        return render(request, 'users/profile.html', {'username': st, 'user': request.user, 'location': 'Profile', 'logout':'../logout', 'form': form})


    address = ContactInformation.objects.get(
        Q(username=request.user.username)
    )

    profile = Profile.objects.get(
        Q(user = request.user.id)
    )

    picture = "/media/%s"%(profile.picture)


    #userProfile = Profile

    #print(address.address_1)

    return render(request, 'users/profile.html', {'username': st, 'user': request.user, 'location': 'Profile', 'logout':'../logout', 'form': form, 'address': address,'picture':picture})
