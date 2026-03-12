from django.urls import path
from .views import predict,test_page, predict_network, pollution_graph

urlpatterns = [
    path('predict/', predict),
    path('test/', test_page),
     path("network/", predict_network),
     path("pollution-graph/", pollution_graph),
]

