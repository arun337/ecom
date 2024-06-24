from . import views
from django.urls import path,include

urlpatterns = [
  
   path('account/',views.show_account,name="account"),
   path('logout/',views.signout,name="logout")
    
]