from django.urls import path
from . import views

urlpatterns = [
    path('manageInterviews_byuser/<int:pk>/', views.getInterviewsbyusers),
    path('manageInterviews/', views.manageInterviewsList),
    path('manageInterviews/<int:pk>/', views.manageInterviewsDetail),
    path('manageusers/', views.manageusersList.as_view()),
    path('manageusers/<int:pk>/', views.manageusersDetail.as_view()),
]