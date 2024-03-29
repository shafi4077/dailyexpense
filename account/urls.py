from django.urls import re_path

from account.views import home, DailyExpenseLogin, daily, weekly, year_to_date, this_week, PayeeSuggestion

urlpatterns = [
    re_path(r'^$', home, name='home'),
    re_path(r'^daily', daily, name='daily'),
re_path(r'^weekly', weekly, name='weekly'),
    re_path(r'^year-to-date', year_to_date, name='year_to_date'),
    re_path(r'^this-week', this_week, name='this_week'),
    re_path(r'^login$', DailyExpenseLogin.as_view(), name='login'),
    re_path(r'^payee-suggestion', PayeeSuggestion.as_view(), name='login'),

]
