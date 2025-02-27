from django.urls import path
from .views import CreateAdminUserViews, DetailAdminUserViews

urlpatterns = [
    path('admin/create/', CreateAdminUserViews.as_view()),
    path('admin/<int:pk>/', DetailAdminUserViews.as_view())
]
