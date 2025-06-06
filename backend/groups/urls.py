from django.urls import path, include
from .views import GroupListCreateView
from . import views
from .views import GroupViewSet,GroupJoinView,GroupPostListCreateView, GroupActivityFeedView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'admin', GroupViewSet)

urlpatterns = [
    path('', GroupListCreateView.as_view(), name='group-list-create'),  
    path('<int:group_id>/', views.group_detail, name='group-detail'),
    path('', include(router.urls)),
    path('<int:pk>/join/', GroupJoinView.as_view(), name='group-join'),   
    path('admin/', include(router.urls)),  
    path('group-posts/', GroupPostListCreateView.as_view(), name='group-posts'),    
    path('group-posts/<int:pk>/like/', views.like_group_post, name='like-group-post'),
    path('group-activity/', GroupActivityFeedView.as_view(), name='group-activity-feed'),

]
