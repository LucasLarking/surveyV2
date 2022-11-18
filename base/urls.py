from django.contrib import admin
from django.urls import path, include

from .views import (
    home,
    createSurvey,
    takeSurvey,
    newQuestion
)


urlpatterns = [
  
    path('', home, name='home'),
    path('createsurvey/<str:pk>', createSurvey, name='createSurvey'),
    path('takesurvey/<str:pk>', takeSurvey, name='takeSurvey'),
    path('newquestion', newQuestion, name='newQuestion'),
]
