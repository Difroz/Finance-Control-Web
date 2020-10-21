import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Bill, Transaction, Category


class BillModelTest(TestCase):
    """
    Тестирование модели "Счет"
    """
    def setUp(self):
        """
        Настройка теста (создание объекта модели)
        :return: объект модели
        """
        self.user = get_user_model().objects.create_user(username='test', password='12345')
        self.user.save()
        self.bill = Bill(
            user=self.user,
            name='test',
            value=100,
            saving=False
        )
        self.bill.save()

    def tearDown(self):
        self.user.delete()

    def test_bill_read(self):
        self.assertEqual(self.bill.user, self.user)
        self.assertEqual(self.bill.name, 'test')
        self.assertEqual(self.bill.value, 100)
        self.assertFalse(self.bill.saving)

    def test_bill_update(self):
        self.bill.name = 'new'
        self.bill.value = 20
        self.bill.saving = True
        self.bill.save()
        self.assertEqual(self.bill.name, 'new')
        self.assertEqual(self.bill.value, 20)
        self.assertTrue(self.bill.saving)

class TransactionModelTest(TestCase):
    """
    Тестирование модели "Транзакции"
    """
    @classmethod
    def setUpTestData(cls):
        """
        Создание объектов для всех медотов класса
        """

        cls.user = get_user_model().objects.create_user(username='test', password='12345')
        Category.objects.create(user=cls.user, name='test')
        cls.category = Category.objects.get()
        Bill.objects.create(
            user=cls.user,
            name='test1',
            value=200,
        )
        cls.bill = Bill.objects.get()
        Transaction.objects.create(
            user=cls.user,
            category=cls.category,
            status='Расход',
            total=50,
            bill=cls.bill,
        )
        cls.transaction = Transaction.objects.get(id=1)


    def setUp(self):
        """
        Создание объектов для каждого медота класса
        """
        pass

    def tearDown(self):
        pass

    def test_transaction_read(self):
        self.assertEqual(self.transaction.user, self.user)
        self.assertEqual(self.transaction.category, self.category)
        self.assertEqual(self.transaction.status, 'Расход')
        self.assertEqual(self.transaction.total, 50)
        self.assertEqual(self.transaction.bill, self.bill)

    def test_transaction_save(self):
        Transaction.objects.create(
            user=self.user,
            category=self.category,
            status='Расход',
            total=50,
            bill=self.bill,
        )
        value = self.bill.value
        self.assertEqual(value, value-self.transaction.total)

    def test_transaction_update(self):
        self.transaction.total = 100
        self.transaction.save()
        value = self.bill.value
        self.assertEqual(value, value-self.transaction.total)




