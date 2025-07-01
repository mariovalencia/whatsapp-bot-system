from django.urls import path
from .views import (AskBotView, IntentManagementView, 
                    IntentUpsertView, TrainNLPView, ResponseListCreateView, 
                    ResponseRetrieveUpdateDestroyView, SetDefaultResponseView, 
                    EvaluateModelView,TaskStatusView,ConversationLogListView)

urlpatterns = [
    path('ask/', AskBotView.as_view(), name='ask_bot'),
    path('intents/', IntentManagementView.as_view(), name="manage_intents"),
    path('intents/upsert/', IntentUpsertView.as_view(), name='upsert_intent'),
    path('train/', TrainNLPView.as_view(), name='train_nlp'),
    path('responses/', ResponseListCreateView.as_view(), name='response-list-create'),
    path('responses/<int:pk>/', ResponseRetrieveUpdateDestroyView.as_view(), name='response-detail'),
    path('intents/<int:intent_id>/set-default-response/', SetDefaultResponseView.as_view(), name='set-default-response'),
    path('evaluate/', EvaluateModelView.as_view(), name='evaluate-model'),
    path('task-status/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
    path('conversations/', ConversationLogListView.as_view(), name='conversation-log-list'),
]