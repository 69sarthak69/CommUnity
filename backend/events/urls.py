from django.urls import path
from .views import (
    EventListCreateView,
    EventJoinView,
    CancelRSVPView,
    event_detail,
    EventUpdateDeleteView,
)

urlpatterns = [
    path('', EventListCreateView.as_view(), name='event-list-create'),                # GET/POST /api/events/
    path('<int:event_id>/', event_detail, name='event-detail'),                      # GET /api/events/<id>/
    path('<int:pk>/join/', EventJoinView.as_view(), name='event-join'),              # POST /api/events/<id>/join/
    path('<int:pk>/cancel/', CancelRSVPView.as_view(), name='event-cancel-rsvp'),    # POST /api/events/<id>/cancel/
    path('<int:pk>/edit/', EventUpdateDeleteView.as_view(), name='event-edit-delete') # PUT/DELETE /api/events/<id>/edit/
]
