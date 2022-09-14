from django.contrib import admin
from django.urls import path, include
from .views import Import, Update, Export

urlpatterns = [
    path('', Import.as_view(), name='test'),
    path('upd/', Update.as_view(), name='update'),
    path('export/', Export.as_view(), name='export'),
]