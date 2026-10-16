from django.urls import path
from .views import (
    RegisterView, LoginView, TicketListCreateView,
    TicketDetailView, TicketSetStatusView, ReplyCreateView
)

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='auth-register'),
    path('auth/login', LoginView.as_view(), name='auth-login'),
    path('tickets', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/set-status', TicketSetStatusView.as_view(), name='ticket-set-status'),
    path('replies', ReplyCreateView.as_view(), name='reply-create'),
]

