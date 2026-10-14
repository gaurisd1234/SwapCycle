from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.ConversationListView.as_view(), name='conversation-list'),
    path('new/<int:user_id>/', views.ConversationCreateView.as_view(), name='conversation-create'),
    path('<int:pk>/', views.ConversationDetailView.as_view(), name='conversation-detail'),
    path('<int:pk>/send/', views.MessageCreateView.as_view(), name='message-create'),
]