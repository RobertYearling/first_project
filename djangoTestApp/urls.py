from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('register', views.register),
    path('login', views.login),
    path('travels', views.travels),
    path('view/<int:tripId>', views.view),
    path('back', views.back),
    path('logout', views.logout),
    path('createTrip', views.createTrip),
    path('addTrip', views.addTrip),
    path('join/<int:tripId>', views.addToTrip),
    path('cancel/<int:tripId>', views.cancelTrip),
    path('deleteTrip/<int:tripId>', views.deleteTrip),
]