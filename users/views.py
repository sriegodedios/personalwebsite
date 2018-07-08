from django.shortcuts import render
from django.contrib.auth import login, authenticate, update_session_auth_hash
#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.forms import SignUpForm, LoginForm, AddressForm, ImageUploadForm, ProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from users.models import ContactInformation, Profile
from django.db.models import Q
from django.contrib.auth.models import User


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

    profile = Profile.objects.get(Q(user = request.user.id))
    picture = "/media/%s"%(profile.picture)

    pictureform = ImageUploadForm(request.user)
    return render(request, 'users/index.html', {'username': st, 'location':'Dashboard', 'logout':'../users/logout', 'picture':picture})

def ajax(request):
    return render(request, 'users/pages/404.html')

@login_required(login_url='/users/login/')
def ResetPassword(request):
    fname = request.user.first_name
    lname = request.user.last_name
    st = "%s %s" %(fname,lname)

    profile = Profile.objects.get(Q(user = request.user.id))

    picture = "/media/%s"%(profile.picture)

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
        'form': form, 'username': st, 'location': 'Profile / Password Reset', 'logout':'../../logout','picture':picture
    })

@login_required(login_url='/users/login/')
def AddressPage(request):
    location = "Profile / Address"
    fname = request.user.first_name
    lname = request.user.last_name
    st = "%s %s" %(fname,lname)
    profile = Profile.objects.get(
        Q(user = request.user.id)
    )
    picture = "/media/%s"%(profile.picture)



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
        'form': form, 'username': st, 'location': location, 'logout':'../../logout', 'picture' : picture
    })

def AddressChange(request):
    location = "Profile / Address / Change"
    fname = request.user.first_name
    lname = request.user.last_name
    st = "%s %s" %(fname,lname)

    user_profile = Profile.objects.get(Q(user=request.user))
    if request.method == "POST":
        address = user_profile.Address
        address.address_1 = request.POST['address_1']
        address.address_2 = request.POST['address_2']
        address.zip_code = request.POST['zip_code']
        address.city = request.POST['city']
        address.state = request.POST['state']

        address.save()
        user_profile.save()
        print(address)
        return redirect('../../profile')



    else:
        Address = user_profile.Address


        form = AddressForm()
        return render(request, 'users/update-address.html', {'username': st, 'user': request.user, 'location': 'Profile', 'logout':'../logout', 'form': form, 'address':Address})

def ProfilePicUpdate(request):
    if request.method == "POST":

        user_profile = Profile.objects.get(Q(user=request.user))
        update_user = ProfileForm(data=request.POST, instance=request.user)
        form = ImageUploadForm(request.POST, instance=user_profile)
        if form.is_valid():

            profile = user_profile

            print(profile)


            profile.picture =request.FILES['picture']


            profile.save()
            return redirect('../../users/profile')

        return HttpResponse("Uh oh22")
        #print(request.POST)
        #profile.picture.picture = request.FILES['picture']
        #profile.picture.name = request.FILES['picture'].name
        #print(request.FILES['picture'])





        #print(profile.picture)



    return HttpResponse("Uh oh")


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

    pictureform = ImageUploadForm(request.user)
    #userProfile = Profile

    #print(address.address_1)

    return render(request, 'users/profile.html', {'username': st, 'user': request.user, 'location': 'Profile', 'logout':'../logout', 'form': form, 'address': address,'picture':picture, 'pictureform':pictureform})
