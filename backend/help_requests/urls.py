from django.urls import path
from .views import (
    HelpRequestListCreateView, HelpRequestDetailView,
    HelpResponseCreateView, HelpResponseListView,
    # NotificationListView, MarkNotificationAsReadView,
    # MarkAllNotificationsAsReadView,
    CommunityPostCreateView, CommunityPostListView,ApplyToHelpView
)


urlpatterns = [
    # Help Requests
    path('help-requests/', HelpRequestListCreateView.as_view(), name='help-request-list-create'),
    path('help-requests/<uuid:pk>/apply/', ApplyToHelpView.as_view(), name='apply-to-help'),
    path('help-requests/<uuid:pk>/', HelpRequestDetailView.as_view(), name='help-request-detail'),
    


    # Help Responses
    path('help-responses/', HelpResponseCreateView.as_view(), name='help-response-create'),
    path('help-responses/<uuid:request_id>/', HelpResponseListView.as_view(), name='help-response-list'),

    path('community-posts/', CommunityPostListView.as_view(), name='list-community-posts'),
    path('community-posts/create/', CommunityPostCreateView.as_view(), name='create-community-post'),

    # Notifications
    # path('notifications/', NotificationListView.as_view(), name='notification-list'),
    # path('notifications/<uuid:notification_id>/read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
    # path('notifications/mark-all-read/', MarkAllNotificationsAsReadView.as_view(), name='mark-all-notifications-read'),
]




