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


def generate_ai_answer(question, answers):
    # Сгенерируем случайное число от 1 до 10 в качестве оценки
    generated_evaluation = str(random.randint(1, 10))

    # Создаем новую запись данных для результата
    question_data = {
        'id': None,  # Вы можете заменить None на фактический идентификатор, если он у вас есть
        'question': question,
        'answers': answers,
        'evaluation': generated_evaluation
    }

    # Сохраняем результат в JSON-файл
    with open('result.json', 'a') as file:
        json.dump(question_data, file)
        file.write('\n')

    return generated_evaluation

def delete_data(request):
    Question.objects.all().delete()
    return JsonResponse({'message': 'Data deleted successfully'})
