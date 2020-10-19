from django.contrib import admin
from django.forms import ModelChoiceField
from .models import Transaction, Category, Bill


class CostAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(user=request.user))
        if db_field.name == 'bill':
            return ModelChoiceField(Bill.objects.filter(user=request.user))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Bill)
admin.site.register(Transaction, CostAdmin)
admin.site.register(Category)