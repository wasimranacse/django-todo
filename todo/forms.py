from dataclasses import fields
from statistics import mode
from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo

        fields = ['title', 'description', 'is_completed']

