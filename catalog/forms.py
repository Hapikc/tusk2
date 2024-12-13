from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import AdvUser
from django.core.validators import RegexValidator
from .models import Application, Categories



class ChangeUserInfoForm(forms.ModelForm):
   email = forms.EmailField(required=True, label='Адрес электронной почты')

   class Meta:
       model = AdvUser
       fields = ('username', 'email', 'last_name', 'first_name', 'patronymic')

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

    last_name = forms.CharField(label='Фамилия', max_length=100, validators=[
        RegexValidator(
            regex=r'^[а-яА-ЯёЁ\s-]+$',
            message='Фафмилия должно состоять только из кириллических букв, пробелов и дефисов.'
        )
    ])

    first_name = forms.CharField(label='Имя', max_length=100, validators=[
        RegexValidator(
            regex=r'^[а-яА-ЯёЁ\s-]+$',
            message='Имя должно состоять только из кириллических букв, пробелов и дефисов.'
        )
    ])

    patronymic = forms.CharField(label='Отчество', max_length=100, validators=[
        RegexValidator(
            regex=r'^[а-яА-ЯёЁ\s-]+$',
            message='Очество должно состоять только из кириллических букв, пробелов и дефисов.'
        )
    ])

    username = forms.CharField(label='Логин', max_length=30, validators=[
        RegexValidator(
            regex=r'^[a-zA-Z-]+$',
            message='Логин должен состоять только из латинских букв и дефисов.'
        )
    ])


    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self): #Метод проверки, если не проходит валидацию, то оччищает данные

        super().clean() #встроенная функция, которая позволяет вызывать методы родительского класса.

        password1 = self.cleaned_data.get('password1') #cleaned_data — это словарь, который содержит
        # валидированные данные из формы. Он доступен только после вызова метода is_valid() и только если данные прошли
        # валидацию.

        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', ValidationError(  # add_error используется для добавления пользовательских
                # сообщений об ошибках в форму.
                'Введенные пароли не совпадают.'
            ))

        cleaned_data = super().clean()
        if not cleaned_data.get('consent'):
            self.add_error('consent', ValidationError('Вы должны согласиться с условиями.'))
        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:  # commit - флаг для сохранения в бд
            user.save()
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'last_name', 'first_name', 'patronymic', 'email', 'password1', 'password2', 'consent')
        widgets = {   #Отвечает за генерацию полей форм в html, можно задавать разные сво-ва и параметры
            'consent': forms.HiddenInput(),
        }

class ApplicationForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Categories.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Application
        fields = ('date', 'name', 'description', 'price', 'categories', 'photo')

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and photo.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Размер фото не должен превышать 2 Мб.")
        if photo.image.format.lower() not in ['jpeg', 'jpg', 'png', 'bmp']:
            raise forms.ValidationError("Формат фото должен быть: jpeg, jpg, png, bmp")
        return photo


class OrderForm(forms.Form):
    applications = forms.ModelMultipleChoiceField(
        queryset=Application.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )