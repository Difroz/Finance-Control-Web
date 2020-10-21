from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from .forms import TransactionForm
from .models import Transaction, Category, Bill


class Index(TemplateView):
    template_name = 'base.html'


class TransactionView(ListView):
    model = Transaction
    template_name = 'main/transaction.html'
    ordering = ['-date']

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return Transaction.objects.filter(user=self.request.user)
        return None


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'main/transaction_add.html'
    form_class = TransactionForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(TransactionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'main/transaction_update.html'

    def get_form_kwargs(self):
        kwargs = super(TransactionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'main/transaction_delete.html'
    success_url = reverse_lazy('cost')


class CategoryView(ListView):
    model = Category
    template_name = 'main/category.html'

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return Category.objects.filter(user=self.request.user)
        return Category.objects.all()


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'main/category_add.html'
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'main/category_update.html'


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'main/category_delete.html'
    success_url = reverse_lazy('category')

    def delete(self, request, *args, **kwargs):
        message ='Невозможно удалить категорию, пока на нее есть сслыка в транзакциях'
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except ProtectedError:
            return render(request, 'main/category_delete_error.html', context={'message': message})


class BillView(ListView):
    model = Bill
    template_name = 'main/bills.html'

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return Bill.objects.filter(user=self.request.user)
        return None


class BillCreateView(LoginRequiredMixin, CreateView):
    model = Bill
    template_name = 'main/bill_add.html'
    fields = ['name', 'value', 'saving']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BillUpdateView(UpdateView):
    model = Bill
    fields = ['name', 'value']
    template_name = 'main/bill_update.html'


class BillDeleteView(DeleteView):
    model = Bill
    template_name = 'main/bill_delete.html'
    success_url = reverse_lazy('bills')

    def delete(self, request, *args, **kwargs):
        message ='Невозможно удалить счет, пока на него есть сслыка в транзакциях'
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except ProtectedError:
            return render(request, 'main/bill_delete_error.html', context={'message': message})


