from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.StatusView.as_view()),
    path('consult/', views.ConsultView.as_view()),
    path('exchange/', views.CurrencyExchangeView.as_view()),
    path('all/', views.CurrencyListAPIView.as_view()),
    path('create/', views.CurrencyCreateAPIView.as_view()),
    path('destroy/<int:pk>/', views.CurrencyDestroyAPIView.as_view()),
    path('update/<int:pk>/', views.CurrencyUpdateAPIView.as_view()),
]