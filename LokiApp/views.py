import os
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm,ImagePostForm
# from PIL import Image as ImageHandle
# "import something" doesn't work with django.Only "from . import something."
from . import image_handle
from . import db_handle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
image_storage_folder = os.path.join(BASE_DIR, 'image_storage')


@login_required
def refresh(request):
	response=HttpResponseRedirect("/")
	response.delete_cookie("isLocationAvailable",path="/")
	return response

@login_required

def account(request):
	return render(request,"account.html",{'username':request.user.username})

@login_required
def feed(request,page_no=1):
	if request.method=="GET":
		# feed/ ,feed/page_no  both come here.
		# feed/ means feed/1.Hence a request with url "feed/1" will never be made.(Since we treat feed/ as feed/1 and show first 10 images).Firstever url with a page_no is "feed/2"(Unless user forces the url feed/1)
		# ToDo :Disallow users to send forced urls(eg feed/2).(Change the scrollview to diff logic.Like loading the image one by one.)
		print("page",page_no)
		page_no=int(page_no)
		# user_ids_and_post_ids=db_handle.get_nearby_posts()
		longitude="blah"
		latitude="blah"
		# I shouldn't have done this(below try catch) now.There are more pressing issues now like feed request for a page that doesn't exist
		try:
			# If cookie says location is available but it's not available due to the rare case in which logout is successful in server side but cookie was not deleted (since the client couldn't receive the cookie delete response)
			longitude=request.session['longitude']
			latitude=request.session['latitude']
		except Exception as e:
			# ToDo if the case explaind in try block happens?
			# print("Cookie SAYS location is available.But it is not.So get the location and then come to feed again.Use a middle view probably.")
			print("location not available.Redirecting to home")
			return redirect("/")
			# -->middle view deletes the cookie "click to home" (cookie del done while showing this)-->home
		else:
			# if no error occurred,this means location is available in session (What cookie said is true)
			print(longitude,"ll")
			print(latitude,"l")
			user_ids_and_post_ids=[]
			isFirstPage=False
			if page_no==1:
				isFirstPage=True
				user_ids_and_post_ids=db_handle.get_nearby_posts(longitude,latitude,page_no)
				# user_ids_and_post_ids=[[user_id,post_id],[user_id,post_id],.......]
				#ToDo an error will occur here.Due to forced url for a feed page that doesn't exist.
			elif page_no>1: #load from pointers
				last_seen_post=request.session['last_seen_post']
				user_ids_and_post_ids=db_handle.get_nearby_posts(longitude,latitude,page_no,last_seen_post[0],last_seen_post[1])
			else:
				return HttpResponse("wrong page no")
			list_len=len(user_ids_and_post_ids)
			print(list_len,"list_len")
			if(list_len==0):
				return HttpResponse("No posts to show")
			elif list_len<10:
				page_no=0
			else:
				# page_no doesn't matter since we use timestamp as pointer.We make it 2 to prevent it from being 1 (if 1,db_handle won't accept user-id and post_id for comparison) and 0 (if 0 ,next page link won't be shown)
				# Though the page no is 2,results will always be different since we use user_id,post_id pointers in session.
				page_no=2
			last_seen_post=[
			user_ids_and_post_ids[list_len-1][0],
			user_ids_and_post_ids[list_len-1][1]
			]
			request.session['last_seen_post']=last_seen_post
			context={'user_ids_and_post_ids':user_ids_and_post_ids,'page_no':page_no}
			if isFirstPage:#Which means page_no was 1 initially.So we set cookie
				print("Storing location flag to cookie..")
				response=render(request,"feed.html",context)
				response.set_signed_cookie('isLocationAvailable',value=True,max_age=None,path='/',httponly=True)
				return response
			return render(request,"feed.html",context)
	else:
		print("Refresh started")
		longitude=float(request.POST.get('longitude'))
		latitude=float(request.POST.get('latitude'))
		# 111 meters accuracy
		longitude=round(longitude,3)
		latitude=round(latitude,3)
		request.session['longitude']=longitude
		request.session['latitude']=latitude
		# ----------
		user_ids_and_post_ids=[]
		isFirstPage=False
		if page_no==1:
			isFirstPage=True
			user_ids_and_post_ids=db_handle.get_nearby_posts(longitude,latitude,page_no)
			# user_ids_and_post_ids=[[user_id,post_id],[user_id,post_id],.......]
			#ToDo an error will occur here.Due to forced url for a feed page that doesn't exist.
		elif page_no>1: #load from pointers
			last_seen_post=request.session['last_seen_post']
			user_ids_and_post_ids=db_handle.get_nearby_posts(longitude,latitude,page_no,last_seen_post[0],last_seen_post[1])
		else:
			return HttpResponse("wrong page no")
		list_len=len(user_ids_and_post_ids)
		print(list_len,"list_len")
		if(list_len==0):
			return HttpResponse("No posts to show")
		elif list_len<10:
			page_no=0
		else:
			# page_no doesn't matter since we use timestamp as pointer.We make it 2 to prevent it from being 1 (if 1,db_handle won't accept user-id and post_id for comparison) and 0 (if 0 ,next page link won't be shown)
			# Though the page no is 2,results will always be different since we use user_id,post_id pointers in session.
			page_no=2
			
		last_seen_post=[
		user_ids_and_post_ids[list_len-1][0],
		user_ids_and_post_ids[list_len-1][1]
		]
		request.session['last_seen_post']=last_seen_post
		context={'user_ids_and_post_ids':user_ids_and_post_ids,'page_no':page_no}
		if isFirstPage:#Which means page_no was 1 initially.So we set cookie
			print("Storing location flag to cookie..")
			response=render(request,"feed.html",context)
			response.set_signed_cookie('isLocationAvailable',value=True,max_age=None,path='/',httponly=True)
			return response
		print("Refresh finished")
		return render(request,"feed.html",context)
		# -------

@login_required
def home(request):
	if request.method=="GET":
		if not request.get_signed_cookie('isLocationAvailable', False):#False is here to suppress the error when cookie is not available.
			# Delete old location values
			if 'longitude' in request.session:
				del request.session['longitude']
			if 'latitude' in request.session:
				del request.session['latitude']
			return render(request,'feed_button_with_location_request.html')
		else:
			# return render(request,'feed_button_without_location_request.html')
			return redirect("/feed/")

	# when user clicks Feed button(it's of SUBMIT type),request will come here.
	elif request.method=="POST":
		# If isLocationAvailable is not set,then that means we have shown them the code which gets location from user.That location will be available in post request.
		if not request.get_signed_cookie('isLocationAvailable', False):#False is here to suppress the error when cookie is not available.
			print("accessing location from user ",request.user.username)
			longitude=float(request.POST.get('longitude'))
			latitude=float(request.POST.get('latitude'))
			# 111 meters accuracy
			longitude=round(longitude,3)
			latitude=round(latitude,3)
			request.session['longitude']=longitude
			request.session['latitude']=latitude
		# if isLocationAvailable is set then,it means location is available in session variable.We access it below.a
		else:
			print("location is available in session.accessing it")
			longitude=request.session['longitude']
			latitude=request.session['latitude']
		print(request.session['longitude'],"longitude")
		print(request.session['latitude'],"latitude")
		# isLocationAvailable cookie is not set here.It's sent with the feed request.
		print("redirecting to feed/1")
		return redirect("/feed/")

def signup(request):
	# ToDo check login and change accordingly
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("/login/signup_success")
		else:
			# print(form.errors)
			# Extract error code from sign-up form :https://stackoverflow.com/a/41711850/9217577
			error_names,error_descriptions=next(iter(form.errors.items())) 
			print(''.join(error_descriptions)) #I don't know how this works.
			error_descriptions=''.join(error_descriptions)
			# ToDo remove helptext in form
			form = RegisterForm()
			return render(request, "signup.html", {"form":form,'message':error_descriptions})
	else:
		form = RegisterForm()
		return render(request, "signup.html", {"form":form})


# Do not change the name from login_view to login.Because default login() function causes problems .
def login_view(request,message=None):
	# ToDo check login and change accordingly
	if request.user.is_authenticated:
			return redirect("/")
	elif request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				# return HttpResponse("Logged in")
				return redirect("/")
			else:
				return render(request,"login.html",{'message':"Your account was inactive."})
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return render(request,"login.html",{'message':"Wrong username or password"})
		# return HttpResponse(request.user.username)
		# return HttpResponse("Already logged in!")
	else:
		print(message,"message")
		if message!=None and message=="signup_success":
			return render(request, 'login.html',{'message':'Account created successfully!..Login to continue!'})
		else:
			return render(request, 'login.html')



# Do not change the name from logout_view to logout.Because default logout() function causes problems 
def logout_view(request):
	# ToDo check login and change accordifngly
	if request.user.is_authenticated:
		logout(request)
		response=render(request,'logout_status.html',{'message':"Logged out successfully"})
		# Why del cookie? bcoz session will be deleted during logout.If this cookie is stil there,we'll try to access location in session which won't be available.
		response.delete_cookie('isLocationAvailable')
		return response
		return render(request,'logout_status.html',{'message':"Logged out successfully"})
	else:
		return render(request,'logout_status.html')


@login_required
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
			if status==True:
				print(request.user.username," has made a post")
				return render(request,"post_status.html",{'status':1})
			else:
				return render(request,"post_status.html",{'status':0})
		else:
			print(form.errors)
			return HttpResponse("form invalid")
	else:
		create_post_form=ImagePostForm()
		return render(request,'create_post.html',{'create_post_form':create_post_form})