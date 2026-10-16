from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_view),
    path('login', views.login_view),
    path('tickets', views.tickets_list_create),
    path('tickets/<int:pk>', views.ticket_detail),
    path('tickets/<int:pk>/replies', views.create_reply),
    path('tickets/<int:pk>/status', views.set_status),
]