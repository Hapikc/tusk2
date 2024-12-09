from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import AdvUser
from django.core.validators import RegexValidator


class ChangeUserInfoForm(forms.ModelForm):
   email = forms.EmailField(required=True, label='Адрес электронной почты')

   class Meta:
       model = AdvUser
       fields = ('username', 'email', 'fio')

class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты', validators=[
    RegexValidator(
        regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        message=' Необходим валидный формат email-адреса'
    )
])

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        label='Пароль (повторно)',
        widget=forms.PasswordInput, help_text='Повторите тот же самый пароль еще раз'
    )
    fio = forms.CharField(label='ФИО', max_length=100, validators=[
        RegexValidator(
            regex=r'^[а-яА-ЯёЁ\s-]+$',
            message='ФИО должно состоять только из кириллических букв, пробелов и дефисов.'
        )
    ])
    username = forms.CharField(label='Логин', max_length=30, validators=[
        RegexValidator(
            regex=r'^[a-zA-Z-]+$',
            message='Логин должен состоять только из латинских букв и дефисов.'
        )
    ])
    consent = forms.BooleanField(label='Согласие на обработку персональных данных')


    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', ValidationError(
                'Введенные пароли не совпадают.'
            ))


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'fio', 'email', 'password1', 'password2')