from django import forms
from .models import Transaction, Category, Bill
from django.contrib.auth.models import User

class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['bill'].queryset = Bill.objects.filter(user=user)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Transaction
        exclude = ['user']
        fields = "__all__"



