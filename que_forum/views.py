# views.py
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import AnswerForm
from django.contrib.auth.decorators import login_required

def question_list(request):
    page = request.GET.get('page', 1)
    response = requests.get(f'https://www.udemy.com/instructor-api/v1/courses/x01bHq3lE73GqxZLN3yPtBHeA==/questions/', headers={'Authorization': f'Bearer {settings.UD_API_KEY}'})
    data = response.json() if response.status_code == 200 else {'results': [], 'next': None, 'previous': None}
    return render(request, 'qa.html', {
        'questions': data['results'],
        'next': data['next'],
        'previous': data['previous']
    })

def question_detail(request, pk):
    response = requests.get(f'https://api.udemy.com/endpoint-for-questions/{pk}', headers={'Authorization': f'Bearer {settings.UD_API_KEY}'})
    question = response.json() if response.status_code == 200 else None

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid() and question:
            answer_data = {
                "detail": form.cleaned_data['detail'],
                "question": pk,
                "posted_by": request.user.id  # Modify as necessary
            }
            post_response = requests.post('https://api.udemy.com/endpoint-for-answers', json=answer_data, headers={'Authorization': f'Bearer {settings.UD_API_KEY}'})
            if post_response.status_code == 201:
                return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm()

    return render(request, 'qa/question_detail.html', {'question': question, 'form': form})
