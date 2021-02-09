from main.models import Transaction, Bill
from django.db.models import Sum
def get_balans(user):
    objects = Bill.objects.filter(user=user, saving=False)
    return objects.aggregate(Sum('value'))['value__sum']







