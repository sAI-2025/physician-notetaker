from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Main chat interface
    path('', views.chat_view, name='chat_view'),

    # API endpoint for full analysis (NER + Sentiment + SOAP)
    path('api/', views.chat_api, name='chat_api'),

    # Quick analysis endpoint for specific analysis types
    path('api/quick/', views.quick_analyze_api, name='quick_analyze'),
]
