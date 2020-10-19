from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
"""
Создание моделей для проекта:
Таблица расходов
Таблица категорий расходов
Таблица доходов
Таблица счетов
Таблица источников доходов
Таблица пользователя
"""
User = get_user_model()


class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Название')
    value = models.IntegerField(verbose_name='Баланс')
    save = models.BooleanField(default=False, verbose_name='Сберегательный')

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('bills')

    class Meta:
        ordering = ['value']
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='Название')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category')


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Transaction(models.Model):
    CHOISE_STATUS = [
        ('Расход', 'Расход'),
        ('Доход', 'Доход'),

    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    status = models.CharField(max_length=6, choices=CHOISE_STATUS, default='Расход', verbose_name='Вид')
    total = models.IntegerField(verbose_name='Сумма')
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT, verbose_name='Счет')
    date = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.was_total = self.total

    def __str__(self):
        return '{}, {} : {}'.format(self.user, self.category.name, str(self.total))

    def get_absolute_url(self):
        return reverse('cost')

    def save(self, *args, **kwargs):
        bill = Bill.objects.get(pk=self.bill.pk)
        if self.status == 'CT':
            if self.pk:
                bill.value = models.F('value') + self.was_total
                bill.save()
                bill.value = models.F('value') - self.total
                bill.save()
                return super(Transaction, self).save(*args, **kwargs)
            else:
                print(self.was_total)
                bill.value = models.F('value')-self.total
                bill.save()
        return super(Transaction, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.status == 'CT':
            bill = Bill.objects.get(pk=self.bill.pk)
            bill.value = models.F('value') + self.total
            bill.save()
            return super(Transaction, self).delete(*args, **kwargs)
        return super(Transaction, self).delete(*args, **kwargs)


    class Meta:
        ordering = ['-date']
        verbose_name = 'Транзация'
        verbose_name_plural = 'Транзакции'
