from django.urls import path
from .views import RegisterView
from .views import CustomLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    # path('user/', UserDetailView.as_view(), name='user-detail'), 
]
