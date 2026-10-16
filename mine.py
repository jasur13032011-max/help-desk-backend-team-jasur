# ════════════════════════════════════════════════════════════════════
# DARS 2: URL routing va views
# ════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────
# 1) blog/views.py - oddiy view'lar
# ─────────────────────────────────────────────────────────────────────

from django.http import HttpResponse


def postlar_royxati(request):
    return HttpResponse("Barcha postlar ro'yxati")


def salomlash(request):
    return HttpResponse("Salom, Django!")


def post_detail(request, post_id):
    return HttpResponse(f"Post ID: {post_id}")

# ─────────────────────────────────────────────────────────────────────
# 2) blog/urls.py - app'ning routing fayli
# ─────────────────────────────────────────────────────────────────────

# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.postlar_royxati, name='post-list'),
#     path('salom/', views.salomlash, name='salomlash'),
#     path('<int:post_id>/', views.post_detail, name='post-detail'),
# ]

# ─────────────────────────────────────────────────────────────────────
# 3) mysite/urls.py - bosh routing fayli
# ─────────────────────────────────────────────────────────────────────

# from django.contrib import admin
# from django.urls import path, include
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('blog/', include('blog.urls')),
# ]

# ─────────────────────────────────────────────────────────────────────
# 4) Ataylab xato - include() qilishni unutish (izohda)
# ─────────────────────────────────────────────────────────────────────

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('blog/', include('blog.urls')) qatori yo'q!
# ]
# mysite.com/blog/ -> ❌ Page not found (404)