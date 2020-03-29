from django.contrib import admin
from django.urls import include, path
from blogs.views import intermediate
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', include('blogs.urls')),
    path('accounts/profile/', intermediate),
    path('', lambda request: redirect('blogs/', permanent=False)),
]
