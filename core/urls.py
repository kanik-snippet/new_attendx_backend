from django.urls import path
from .views import *

urlpatterns = [
path("", qr_test_page, name="qr_test"),
]