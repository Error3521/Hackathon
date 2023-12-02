import json
import random

from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render

from .forms import UploadFileForm
from .models import Question


def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_content = request.FILES['file'].read().decode('utf-8')
            json_data = json.loads(file_content)
            Question.objects.all().delete()
            for item in json_data:
                try:
                    # Пытаемся создать объект Question
                    question_obj = Question.objects.create(
                        id=item['id'],
                        question=item['question'],
                        answers=item['answers'],
                        result=str(random.randint(1, 10))
                    )
                except IntegrityError:
                    pass
            avg_result = Question.objects.aggregate(Avg('result'))['result__avg']
            avg_result_rounded = round(avg_result, 2) if avg_result is not None else None
            questions = Question.objects.all()

            context = {'form': form, 'questions': questions, 'avg_result': avg_result_rounded}
            return render(request, 'hackathon/Result.html', context)
    else:
        form = UploadFileForm()

    questions = Question.objects.all()
    avg_result = Question.objects.aggregate(Avg('result'))['result__avg']
    avg_result_rounded = round(avg_result, 2) if avg_result is not None else None

    context = {'form': form, 'questions': questions, 'avg_result': avg_result_rounded}
    return render(request, 'hackathon/Result.html', context)


def generate_result(request):
    questions = Question.objects.all()

    result_data = [{'question': question.question, 'result': question.result} for question in questions]

    avg_result = questions.aggregate(Avg('result'))['result__avg']

    for i, question in enumerate(questions):
        question.result = str(random.randint(1, 10))
        question.save()

    with open('result.json', 'a') as file:
        for data in result_data:
            json.dump(data, file)
            file.write('\n')

    with open('result.json', 'a') as file:
        json.dump({'average_result': avg_result}, file)
        file.write('\n')

    return JsonResponse(result_data, safe=False)


def delete_data(request):
    Question.objects.all().delete()
    return JsonResponse({'message': 'Data deleted successfully'})
