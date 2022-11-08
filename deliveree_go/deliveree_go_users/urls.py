from django.urls import path,include
from deliveree_go_users import viewsets

urlpatterns = [
    path('addressAfterLogin',viewsets.addressAfterLogin.as_view()),
    path('shopData',viewsets.shopData.as_view()),
    path('home_pageApi',viewsets.home_pageApi.as_view()),
    path('itemsListData',viewsets.itemsListData.as_view()),
    path('shopsListData',viewsets.shopsListData.as_view()),
    path('cart_list',viewsets.cart_list.as_view()),
    
]
