from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='home'),
    url(r'^cost/$', views.TransactionView.as_view(), name='cost'),
    url(r'^cost/add/$', views.TransactionCreateView.as_view(), name='cost_add'),
    url(r'^cost/(?P<pk>[-\w]+)/update/$', views.TransactionUpdateView.as_view(), name='cost_update'),
    url(r'^cost/(?P<pk>[-\w]+)/delete/$', views.TransactionDeleteView.as_view(), name='cost_delete'),
    url(r'^category/$', views.CategoryView.as_view(), name='category'),
    url(r'^category/add/$', views.CategoryCreateView.as_view(), name='category_add'),
    url(r'^category/(?P<pk>[-\w]+)/update/$', views.CategoryUpdateView.as_view(), name='category_update'),
    url(r'^category/(?P<pk>[-\w]+)/delete/$', views.CategoryDeleteView.as_view(), name='category_delete'),
    url(r'^bills/$', views.BillView.as_view(), name='bills'),
    url(r'^bill/add/$', views.BillCreateView.as_view(), name='bill_add'),
    url(r'^bill/(?P<pk>[-\w]+)/update/$', views.BillUpdateView.as_view(), name='bill_update'),
    url(r'^bill/(?P<pk>[-\w]+)/delete/$', views.BillDeleteView.as_view(), name='bill_delete'),

]