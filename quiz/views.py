from rest_framework import generics
from rest_framework.response import Response
from .models import Quizzes, Question
from .serializers import QuizSerializer, RandomQuestionSerializer, QuestionSerializer
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from quiz.models import Question, Answer
from django.http import JsonResponse


class Quiz(generics.ListAPIView):

    serializer_class = QuizSerializer
    queryset = Quizzes.objects.all()

class RandomQuestion(APIView):

    def get(self, request, format=None, **kwargs):
        question = Question.objects.filter(quiz__title=kwargs['topic']).order_by('?')[:1]
        serializer = RandomQuestionSerializer(question, many=True)
        return Response(serializer.data)

class QuizQuestion(APIView):

    def get(self, request, format=None, **kwargs):
        quiz = Question.objects.filter(quiz__title=kwargs['topic'])
        serializer = QuestionSerializer(quiz, many=True)
        return Response(serializer.data)
    

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'quiz/questions.html', {'questions': questions})



def submit_answers(request):
    if request.method == "POST":
        user_answers = {}
        for key, value in request.POST.items():
            if key.startswith("question_"):  # Extract answers from form data
                try:
                    question_id = int(key.split("_")[1])
                    answer_id = int(value)
                    user_answers[question_id] = answer_id
                except ValueError:
                    continue  # Skip invalid data

        # Fetch correct answers
        correct_answers = {
            q.id: q.answer.filter(is_right=True).first() for q in Question.objects.all()
        }

        # Calculate score and store per-question results
        score = 0
        results = []
        for q_id, a_id in user_answers.items():
            try:
                question = Question.objects.get(id=q_id)
                user_answer = Answer.objects.get(id=a_id).answer_text
            except (Question.DoesNotExist, Answer.DoesNotExist):
                continue  # Skip invalid answers

            correct_answer_obj = correct_answers.get(q_id)
            correct_answer_text = correct_answer_obj.answer_text if correct_answer_obj else "No correct answer"
            is_correct = correct_answer_obj and correct_answer_obj.id == a_id

            if is_correct:
                score += 1

            results.append({
                'question': question.title,
                'user_answer': user_answer,
                'correct_answer': correct_answer_text,
                'is_correct': is_correct
            })

        return JsonResponse({
            'score': score,
            'total': len(correct_answers),
            'results': results
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)
