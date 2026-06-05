from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
        )

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        # Удаляем пробелы, скобки, тире
        cleaned = ''.join(filter(str.isdigit, phone))

        # Добавляем + в начало
        if cleaned.startswith('375'):
            cleaned = '+' + cleaned
        elif cleaned.startswith('80'):  # если ввели 8044...
            cleaned = '+375' + cleaned[2:]

        # Проверяем формат
        import re
        if not re.match(r'^\+375(25|29|33|44)\d{7}$', cleaned):
            raise forms.ValidationError("Введите номер в формате +375447410212")

        return cleaned
