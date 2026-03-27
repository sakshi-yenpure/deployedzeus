from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('history/', views.chat_history, name='chat_history'),
    path('quality-report/', views.quality_report, name='quality_report'),
    path('refresh-quality-report/', views.refresh_quality_report, name='refresh_quality_report'),
    path('download-quality-report/', views.download_quality_report, name='download_quality_report'),
    path('all-stock-sentiment/', views.all_stock_sentiment, name='all_stock_sentiment'),
]
