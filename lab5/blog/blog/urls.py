from django.contrib import admin
from django.urls import path, re_path
from articles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.archive, name='archive'),
    path('advert/new/', views.create_advert, name='create_advert'),
    re_path(r'^advert/(?P<advert_id>\d+)$', views.get_advert, name='get_advert'),
]
