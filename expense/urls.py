from django.urls import re_path

from expense.views import categories, AddTransaction

urlpatterns = [
    re_path(r'^categories/$', categories, name='cats'),
    re_path(r'^transaction/$', AddTransaction.as_view(), name='txns'),
]
