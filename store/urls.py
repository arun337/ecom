
from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name="index"),
    path('category/',views.category,name="category"),
    path('collections/<str:slug>',views.collection,name="collections"),
    path('collections/<str:cate_slug>/<str:prod_slug>',views.productdetail,name="productdetail"),
    path ('add-to-cart',views.addtocart, name="addtocart"),
    path('cart/',views.cart,name="cart"),
    path('update',views.updatecart,name="update-cart"),
    path('delete',views.deletecartitem,name="delete-cart-item"),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('add-to-wishlist',views.viewwish,name="addtowishlist"),
    path('wishdelete',views.deleteitem,name="wishdelete"),
    path('checkout/',views.checkout,name="checkout"),

    path('placeorder/',views.placeorder,name="placeorder"),
    path('proccedtopay',views.proccedtopay,name="proccedtopay"),
    path('myorder/',views.myorder,name="myorder"),
    path('vieworder/<str:t_no>',views.vieworder,name="vieworder"),
    path('complete/', views.paymentComplete, name="complete"),
    
    
]          