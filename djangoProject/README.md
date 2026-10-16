# Help Desk System (Backend)

## O'rnatish va ishga tushirish buyruqlari

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 5000
# Help Desk Backend API

Help Desk tizimi uchun yaratilgan Django REST Framework va JWT token autentifikatsiyasiga asoslangan backend API loyihasi.

## Loyihada mavjud endpointlar

### Autentifikatsiya:
* `POST /api/auth/register` - Yangi foydalanuvchini ro'yxatdan o'tkazish
* `POST /api/auth/login` - Tizimga kirish va JWT token olish (`token` va `username` qaytaradi)

### Tiketlar (Tickets):
* `GET /api/tickets` - Barcha tiketlar ro'yxatini olish
* `POST /api/tickets` - Yangi tiket yaratish
* `GET /api/tickets/<id>` - Bitta tiket haqida batafsil ma'lumot olish
* `PATCH /api/tickets/<id>/set-status` - Tiket statusini o'zgartirish (`open`, `in_progress`, `closed`)

### Javoblar (Replies):
* `POST /api/replies` - Tiketga javob qaytarish/yozish

---

## Ishga tushirish ko'rsatmalari

1. Virtual muhitni yaratish va faollashtirish:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
## Testlarni ishga tushirish (API endpointlar va validatsiyani tekshirish)

```bash
python manage.py test api
---

### Endi PyCharm terminalida mahalliy ravishda testni va Git'ni bajaramiz:

1. Terminalda quyidagi buyruqni berib ko'ring:
   ```bash
   python manage.py test api
# Help Desk Backend API

Help Desk tizimi uchun yaratilgan Django REST Framework va JWT token autentifikatsiyasiga asoslangan backend API loyihasi. Loyihada barcha kerakli endpointlar, validatsiyalar va token autentifikatsiyasi to'liq amalga oshirilgan.

---

## API Endpointlari va Ishlash Tartibi

### 1. Autentifikatsiya (Authentication)

* **Register (Ro'yxatdan o'tish)**
  * **Endpoint:** `POST /api/auth/register`
  * **Request Body:**
    ```json
    {
      "username": "jasur",
      "password": "password123",
      "email": "jasur@example.com"
    }
    ```
  * **Response (201 Created):**
    ```json
    {
      "username": "jasur",
      "email": "jasur@example.com"
    }
    ```

* **Login (Tizimga kirish va Token olish)**
  * **Endpoint:** `POST /api/auth/login`
  * **Request Body:**
    ```json
    {
      "username": "jasur",
      "password": "password123"
    }
    ```
  * **Response (200 OK):**
    ```json
    {
      "token": "<JWT_ACCESS_TOKEN>",
      "username": "jasur"
    }
    ```

---

### 2. Tiketlar (Tickets)

* **Tiketlar ro'yxatini olish (List Tickets)**
  * **Endpoint:** `GET /api/tickets`
  * **Response (200 OK):** Tiketlar ro'yxati qaytadi.

* **Yangi tiket yaratish (Create Ticket)**
  * **Endpoint:** `POST /api/tickets`
  * **Header:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
  * **Request Body:**
    ```json
    {
      "title": "Kompyuter yoqilmayapti",
      "description": "Tizim bloki quvvatga ulanmagan va chiroq yonmayapti"
    }
    ```

* **Bitta tiket haqida batafsil ma'lumot (Get Ticket Detail)**
  * **Endpoint:** `GET /api/tickets/<id>`

* **Tiket statusini o'zgartirish (Update Ticket Status)**
  * **Endpoint:** `PATCH /api/tickets/<id>/set-status`
  * **Header:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
  * **Request Body:**
    ```json
    {
      "status": "in_progress"
    }
    ```
  * *(Ruxsat etilgan statuslar: `open`, `in_progress`, `closed`)*

---

### 3. Javoblar (Replies)

* **Tiketga javob yozish (Create Reply)**
  * **Endpoint:** `POST /api/replies`
  * **Header:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
  * **Request Body:**
    ```json
    {
      "ticket": 1,
      "body": "Muammo ustida ishlanmoqda"
    }
    ```

---

## Ishga tushirish va Test qilish ko'rsatmalari

1. Virtual muhitni yaratish va faollashtirish:
```bash
python -m venv .venv
# Windows uchun:
.venv\Scripts\activate
# Linux/Mac uchun:
source .venv/bin/activate
---

### 2. `api/views.py` (Barcha Endpointlar va Validatsiya/Autentifikatsiya)

```python
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

        if not username or not password:
            return Response(
                {'error': 'Username va password kiritilishi shart'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'username': user.username
            }, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Login yoki parol noto‘g‘ri'},
            status=status.HTTP_400_BAD_REQUEST
        )


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
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ReplyCreateView(generics.CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)