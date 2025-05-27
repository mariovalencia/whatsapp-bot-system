from django.urls import path
from .views import AskBotView, IntentManagementView, IntentUpsertView

urlpatterns = [
    path('ask/', AskBotView.as_view(), name='ask_bot'),
    path('intents/', IntentManagementView.as_view(), name="manage_intents"),
    path('intents/upsert/', IntentUpsertView.as_view(), name='upsert_intent'),
]