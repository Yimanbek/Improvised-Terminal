from django.urls import path
from .views import ProductCreateViews, ListProductViews, DetailProductViews

urlpatterns = [
    path('create/', ProductCreateViews.as_view()),
    path('<int:pk>/detail/', DetailProductViews.as_view()),
    path('', ListProductViews.as_view())
]
