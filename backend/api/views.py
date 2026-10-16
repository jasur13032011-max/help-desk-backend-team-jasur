from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import Ticket, Reply


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password or len(password) < 6:
        return Response({"error": "Parol kamida 6 ta belgidan iborat bo'lishi kerak!"},
                        status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Foydalanuvchi allaqachon mavjud!"}, status=status.HTTP_400_BAD_REQUEST)

    User.objects.create_user(username=username, password=password)
    return Response({"message": "Muvaffaqiyatli ro'yxatdan o'tdingiz"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Login yoki parol noto'g'ri!"}, status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "username": user.username})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tickets_list_create(request):
    if request.method == 'GET':
        tickets = Ticket.objects.all()
        data = [{"id": t.id, "title": t.title, "status": t.status} for t in tickets]
        return Response(data)

    elif request.method == 'POST':
        title = request.data.get('title')
        body = request.data.get('body')

        if not title or not body:
            return Response({"error": "Sarlavha va matn kiritilishi shart!"}, status=status.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.create(user=request.user, title=title, body=body)
        return Response({"id": ticket.id, "status": ticket.status}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    replies = [{"id": r.id, "text": r.text} for r in ticket.replies.all()]

    data = {
        "id": ticket.id,
        "title": ticket.title,
        "body": ticket.body,
        "status": ticket.status,
        "replies": replies
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reply(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    text = request.data.get('text')

    if not text:
        return Response({"error": "Matn kiritilmadi!"}, status=status.HTTP_400_BAD_REQUEST)

    reply = Reply.objects.create(ticket=ticket, user=request.user, text=text)
    return Response({"id": reply.id}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def set_status(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    new_status = request.data.get('status')

    if new_status not in ['open', 'in_progress', 'closed']:
        return Response({"error": "Noto'g'ri status!"}, status=status.HTTP_400_BAD_REQUEST)

    ticket.status = new_status
    ticket.save()
    return Response({"id": ticket.id, "status": ticket.status})
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Ticket, Reply
from .serializers import (
    RegisterSerializer, TicketSerializer, TicketCreateSerializer,
    TicketStatusSerializer, ReplySerializer, ReplyCreateSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Login yoki parol noto‘g‘ri'}, status=status.HTTP_400_BAD_REQUEST)


class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketCreateSerializer
        return TicketSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TicketDetailView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'


class TicketSetStatusView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketStatusSerializer
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ReplyCreateView(generics.CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Xato maʼlumot kiritildi'}, status=status.HTTP_400_BAD_REQUEST)