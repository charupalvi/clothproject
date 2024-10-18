"""
clothapp urls.py file :-
"""
from django.urls import path
from clothapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home),
    path('register',views.register),
    path('login',views.userLogin),
    path('about',views.about),
    path('contact',views.contact),
    path('details/<int:clothid>',views.clothDetails),
    path('logout',views.userLogout),
    path('searchcat/<str:cat>',views.searchByCat),
    path('searchbyprice',views.searchByRange),
    path('sort/<int:dir>',views.sortClothsByPrice),
    path('addtocart/<int:clothid>',views.addToCart),
    path('mycart',views.showMyCart),
    path('removecart/<int:cartid>',views.removeCart),
    path('updatecount/<int:cartid>/<str:oprn>',views.updateQuantity),
    path('confirmorder',views.confirmOrder),
    path('profile',views.editProfile),
    path('makepayment',views.makePayment),
    path('placeorder/<str:oid>',views.placeOrder),

]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)