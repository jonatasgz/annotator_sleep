from django.urls import path
from . import views

urlpatterns = [
    path("get_episode", views.get_episode, name = "get_episode"),
    path("submit_episode", views.submit_episode, name = "submit_episode"),
    path("ner", views.ner, name = "ner"),
    path("predict", views.predict, name = "predict"),
    path('highlights', views.highlights, name='highlights'),
    path('delete_highlight/<int:pk>/', views.delete_highlight, name='delete_highlight'),
    path('download_db', views.download_db, name='download_db'),
    path('download_predictions', views.download_predictions, name='download_predictions'),     
]