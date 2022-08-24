from django.urls import path
from . import views
urlpatterns = [

     path('check/<int:id>',views.check,name='check'),   
     path('addnew',views.addnew,name='addnew'),
     path('savedata',views.savedata,name='savedata'),
     path('updatedata/<int:id>',views.updatedata,name='updatedata'),
     path('trans',views.trans,name='trans'), 
     path('trascheck/<int:id>',views.trascheck,name='trascheck'), 
     
]