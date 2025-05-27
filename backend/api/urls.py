from django.urls import path
from bot_management.views import AskBotView

urlpatterns = [
    path('ask/', AskBotView.as_view(), name='ask_bot'),
]