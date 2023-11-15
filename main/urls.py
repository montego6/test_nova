from django.urls import path
from .views import CreateFileInDriveAPIView

urlpatterns = [
    path('create_file/', CreateFileInDriveAPIView.as_view(), name='create-file'),
]