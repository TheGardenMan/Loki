import os
from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm,ImagePostForm
# from PIL import Image as ImageHandle
# The below lines fucks up sometimes.I don't know why.It may say moduleNotFound
from . import image_handle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
image_storage_folder = os.path.join(BASE_DIR, 'image_storage')

def home(request):
	# ToDo check login and change accordifngly
	return render(request, 'home.html')

def signup(request):
	# ToDo check login and change accordifngly
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse("done!")
		else:
			print(form.errors)
			return HttpResponse(form.errors)
	else:
		form = RegisterForm()
		return render(request, "signup.html", {"form":form})
# Do not change the name from login_view to login.Because default login() function causes problems .
def login_view(request):
	# ToDo check login and change accordifngly
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponse("Logged in")
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details given")
	elif request.user.is_authenticated:
		return HttpResponse(request.user.username)
		return HttpResponse("Already logged in!")
	else:
		return render(request, 'login.html')
# Do not change the name from logout_view to logout.Because default logout() function causes problems .
def logout_view(request):
	# ToDo check login and change accordifngly
	logout(request)
	return render(request,'logout_success.html')

def create_post(request):
	if request.method=='POST':
		form=ImagePostForm(request.POST,request.FILES)
		longitude=form.data['longitude']
		latitude=form.data['latitude']
		if form.is_valid():
			username=request.user.username
			image_received=form.cleaned_data['image_to_upload']
			status=image_handle.clean_and_store(image_received,username,longitude,latitude)
			# image_in_PIL=ImageHandle.open(image_received)
			# image_in_PIL=image_in_PIL.convert('RGB')
			# image_in_PIL.save(image_storage_folder,'JPEG',quality=50)

			# print(latitude,longitude)
			# return redirect("/")
			return HttpResponse("form valid")
		else:
			print(form.errors)
			return HttpResponse("form invalid")
	else:
		create_post_form=ImagePostForm()
		return render(request,'create_post.html',{'create_post_form':create_post_form})