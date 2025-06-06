from django.urls import path
from .views import (
    HelpRequestListCreateView, HelpRequestDetailView,
    HelpResponseCreateView, HelpResponseListView,
    approve_applicant, reject_applicant,
    CommunityPostCreateView, CommunityPostListView,ApplyToHelpView, HelpApplicationListView, CommentListCreateAPIView, MyHelpApplicationsListView
)



urlpatterns = [
    # Help Requests
    path('help-requests/', HelpRequestListCreateView.as_view(), name='help-request-list-create'),
    path('help-requests/<uuid:pk>/apply/', ApplyToHelpView.as_view(), name='apply-to-help'),
    path('help-requests/<uuid:pk>/', HelpRequestDetailView.as_view(), name='help-request-detail'),
    path('<uuid:pk>/applications/', HelpApplicationListView.as_view(), name='view-applicants'),
    


    # Help Responses
    path('help-responses/', HelpResponseCreateView.as_view(), name='help-response-create'),
    path('help-responses/<uuid:request_id>/', HelpResponseListView.as_view(), name='help-response-list'),

    path('community-posts/', CommunityPostListView.as_view(), name='list-community-posts'),
    path('community-posts/create/', CommunityPostCreateView.as_view(), name='create-community-post'),

    path('comments/', CommentListCreateAPIView.as_view(), name='comments'),

    path('applications/<int:application_id>/approve/', approve_applicant, name='approve-applicant'),
    path('applications/<int:application_id>/reject/', reject_applicant, name='reject-applicant'),

    path('my-applications/', MyHelpApplicationsListView.as_view(), name='my-applications'),
]




