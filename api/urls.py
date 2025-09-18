from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('functions/', views.list_functions, name='list_functions'),
    path('execute/', views.execute_function, name='execute_function'),
    path('tasks/<int:task_id>/', views.task_status, name='task_status'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]