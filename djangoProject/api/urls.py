from django.urls import path
from .views import (
    RegisterView, LoginView, TicketListCreateView,
    TicketDetailView, TicketSetStatusView, ReplyCreateView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/status/', TicketSetStatusView.as_view(), name='ticket-status'),
    path('replies/', ReplyCreateView.as_view(), name='reply-create'),
]