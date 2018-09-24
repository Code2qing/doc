from django.urls import path
from . import views
app_name = 'myaccount'
urlpatterns = [
	path(r'profile/',views.profile,name='profile'),
	path(r'profile/update/',views.profile_update,name='profile_update'),
]