from django.urls import path
from .views import predict,test_page

urlpatterns = [
    path('predict/', predict),
    path('test/', test_page),
]

