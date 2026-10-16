# ════════════════════════════════════════════════════════════════════
# DARS 1: Django'ga kirish va MTV arxitekturasi
# ════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────
# 1) Loyiha va app yaratish (terminal buyruqlari, izohda)
# ─────────────────────────────────────────────────────────────────────

# django-admin startproject mysite
# cd mysite
# python manage.py startapp blog
# python manage.py runserver

# ─────────────────────────────────────────────────────────────────────
# 2) mysite/settings.py - appni ro'yxatdan o'tkazish
# ─────────────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]

# ─────────────────────────────────────────────────────────────────────
# 3) blog/views.py - birinchi view (MTV'dagi View qismi)
# ─────────────────────────────────────────────────────────────────────

from django.http import HttpResponse


def salomlash(request):
    return HttpResponse("Salom, Django!")

# ─────────────────────────────────────────────────────────────────────
# 4) Ataylab xato - INSTALLED_APPS'ga qo'shishni unutish (izohda)
# ─────────────────────────────────────────────────────────────────────

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     # 'blog' qatori yo'q!
# ]
# python manage.py makemigrations blog
# ❌ App 'blog' could not be found. Is it in INSTALLED_APPS?