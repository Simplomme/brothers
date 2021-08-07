from django.urls import re_path
from . import views

app_name="login"
urlpatterns = [
    re_path('^$',views.onLogin,name='login'),
    re_path('^logout/$',views.logout,name='logout'),
]
