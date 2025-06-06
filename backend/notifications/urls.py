from django.urls import path
from .views import NotificationListView, MarkNotificationReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
    path('<uuid:pk>/mark-read/', MarkNotificationReadView.as_view(), name='mark_notification_as_read'),
]

