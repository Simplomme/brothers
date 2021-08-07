from django.urls import re_path
from . import views

app_name='dashboard'
urlpatterns=[
    re_path('^$',views.onDashboard,name='dashboard'),
    re_path('^actualise/$',views.actualiseData,name='actualise'),
    re_path('^vol-stock/$',views.vol_stock,name='vol-stock'),
    re_path('^articles-critiques/$',views.critique,name='articles-critiques'),
    re_path('^purchase/$',views.purchase,name='purchase'),
    re_path('^sell/$',views.sell,name='sell'),
    re_path('^perte/$',views.perte,name='perte'),
    re_path('^purchase-pdf/$',views.printPurchase,name='purchasePDF'),
    re_path('^sell-pdf/$',views.printSell,name='sellPDF'),
    re_path('^perte-pdf/$',views.printPerte,name='pertePDF'),
]
