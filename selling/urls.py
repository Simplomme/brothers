from django.urls import re_path
from . import views


app_name='selling'
urlpatterns=[
        re_path('^$',views.onSelling,name='selling'),
        re_path('^data/$',views.getData,name='getData'),
        re_path('^commandes/$',views.getCmd,name='commandes'),
        re_path('^delete/$',views.deleteCmd,name='delete'),
        re_path('^save/$',views.save,name='save'),
        re_path('^cancel/$',views.cancel,name='cancel'),
        re_path('^daily-log/$',views.onDailyLog,name='dailylog'),
        re_path('^daily-log-pdf/$',views.printFiche,name='dailylogPDF'),
        re_path('^show-facture/$',views.showFacture,name='showFacture'),
        re_path('^facture-pdf/$',views.printFacture,name='facturePDF'),
]
