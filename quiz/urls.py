from django.urls import path
from .views import Quiz, RandomQuestion, QuizQuestion, question_list, submit_answers
from . import views
app_name='quiz'

urlpatterns = [
    path('', Quiz.as_view(), name='quiz'),
    path('r/<str:topic>/', RandomQuestion.as_view(), name='random' ),
    path('q/<str:topic>/', QuizQuestion.as_view(), name='questions' ),
    path('questions/', question_list, name='question_list'),
    path('submit/', submit_answers, name='submit_answers'),
]