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