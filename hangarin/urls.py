from django.contrib import admin
from django.urls import path, include
from tasks.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('tasks/', include('tasks.urls')),
    path('admin/', admin.site.urls),
]