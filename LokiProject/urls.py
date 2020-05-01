from django.contrib import admin
from django.urls import path
from LokiApp import views

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', views.home, name="home"),
	path('signup/', views.signup, name="signup"),
	path('login/', views.login_view, name="login"),
	path('login/<message>', views.login_view, name="login"),
	path('account/', views.account, name="account"),
	path('create_post/', views.create_post, name="create_post"),
	path('feed/',views.feed,name="feed"),
	path('feed/<page_no>/',views.feed,name="feed"),
	path('refresh/',views.refresh,name="refresh"),
	path('logout/', views.logout_view, name="logout"),

]

