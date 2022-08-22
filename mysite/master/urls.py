from django.urls import path
from . import views
urlpatterns = [

     path('',views.hello,name='index'), 
     path('check/<int:id>',views.check,name='check'),   
     path('addnew',views.addnew,name='addnew'),
]