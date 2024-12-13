from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class AdvUser(AbstractUser):
   is_activated = models.BooleanField(default=True, db_index=True,verbose_name='Прошел активацию?')
   last_name = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')
   first_name = models.CharField(max_length=100, blank=True, verbose_name='Имя')
   patronymic = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
   consent = models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных')


   class Meta(AbstractUser.Meta):
       pass


class Categories(models.Model):
   name = models.CharField(max_length=200, help_text="Введите категории")

   def __str__(self):
      return self.name


class Application(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
   date = models.DateField(null=True, blank=True)
   name = models.CharField(max_length=100, blank=True,verbose_name='Название')
   description = models.TextField(max_length=100, verbose_name='описание')
   categories = models.ManyToManyField(Categories, help_text='Описание')
   price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Цена')
   photo = models.ImageField(null=True, upload_to='photos/')
   comment = models.TextField(null=True, blank=True, verbose_name='Комментарий администратора')

   LOAN_STATUS = (
      ('n', 'Новая'),
      ('o', 'Принята в работу'),
      ('d', 'Выполнена'),

   )

   status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='n', help_text="Статус заявки")

   def __str__(self):
      return self.name


class Order(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)
   total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class OrderItem(models.Model):
   order = models.ForeignKey(Order, on_delete=models.CASCADE)
   application = models.ForeignKey(Application, on_delete=models.CASCADE)
   price = models.DecimalField(max_digits=10, decimal_places=2)


