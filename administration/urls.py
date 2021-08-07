from django.urls import re_path
from . import views

app_name='administration'

urlpatterns =[
re_path('articles/$',views.onArticle,name='articles'),
re_path('articles/list/$',views.articlesListe,name='articlesListe'),
re_path('articles/id/$',views.getArticle,name='getArticle'),
re_path('articles/id/delete/$',views.deleteArticle,name='deleteArticle'),
re_path('^stock/$',views.onStock,name='stock'),
re_path('^stock/getDayEntrance/$',views.getDayEntrance,name='getDayEntrance'),
re_path('^users/$',views.newUsers,name='users'),
re_path('^users/list/$',views.usersList,name='usersList'),
re_path('^users/id/$',views.getUser,name='getUser'),
re_path('^users/id/delete/$',views.deleteUser,name='deleteUser'),
re_path('^fiche-inventaire/$',views.printPDF,name='fiche'),
re_path('^ajustement/$',views.ajuster,name='ajuster'),
re_path('^exec-ajuster/$',views.execAjuster,name='execAjuster'),
re_path('^others/$',views.others,name='others'),
re_path('^others-list/$',views.othersList,name='othersList'),
]
