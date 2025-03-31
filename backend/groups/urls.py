from django.urls import path, include
from .views import GroupListCreateView
from . import views
from .views import GroupViewSet,GroupJoinView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'admin', GroupViewSet)

urlpatterns = [
    path('', GroupListCreateView.as_view(), name='group-list-create'),  # handles GET & POST
    path('<int:group_id>/', views.group_detail, name='group-detail'),
    path('', include(router.urls)),
    path('<int:pk>/join/', GroupJoinView.as_view(), name='group-join'),   
    path('admin/', include(router.urls)),      
]
