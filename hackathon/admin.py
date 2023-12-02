# hackathon/admin.py

from django.contrib import admin
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'result')  # Определите поля, которые вы хотите видеть в списке объектов в админке
    search_fields = ('id', 'question')  # Поля, по которым можно производить поиск
    readonly_fields = ('id', 'question', 'answers')  # Поля, которые вы хотите сделать только для чтения
