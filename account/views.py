from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Sum, FloatField, Q, F
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.views import View

from expense.models import Transaction as Txn


# Create your views here.
class DailyExpenseLogin(View):
    def get(self, request):
        return render(request, 'login.html')


@login_required
def home(request):
    user = request.user
    import datetime
    from datetime import timedelta
    today = datetime.date.today()
    week = today - datetime.timedelta(today.weekday())
    month = today.replace(day=1)
    month_end = today.replace(month=week.month+1, day=1) + timedelta(-1)
    year = today.replace(month=1, day=1)

    total = Txn.objects.filter(user=user).aggregate(
        total_income=Coalesce(Sum(Case(
            When(Q(transaction_type=1), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        total_expense=Coalesce(Sum(Case(
            When(Q(transaction_type=2), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        today_income=Coalesce(Sum(Case(
            When(Q(transaction_type=1, transaction_datetime__date=today), then=F('amount')),
            output_field=FloatField(),
            default=0
        )), 0.0),
        today_expense=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__date=today), then=F('amount')),
            output_field=FloatField(),
            default=0
        )), 0.0),
        week_income=Coalesce(Sum(Case(
            When(Q(
                transaction_type=1,
                transaction_datetime__date__gte=week,
                transaction_datetime__date__lte=today
            ), then=F('amount')),
            output_field=FloatField(),
            default=0
        )), 0.0),
        week_expense=Coalesce(Sum(Case(
            When(Q(
                transaction_type=2,
                transaction_datetime__date__gte=week,
                transaction_datetime__date__lte=today
            ), then=F('amount')),
            output_field=FloatField(),
            default=0
        )), 0.0),
        month_income=Coalesce(Sum(Case(
            When(Q(
                transaction_type=1,
                transaction_datetime__date__gte=month,
                transaction_datetime__date__lte=month_end
            ), then=F('amount')),
            output_field=FloatField(),
            default=0
        )), 0.0),
        month_expense=Coalesce(Sum(Case(
            When(Q(
                transaction_type=2,
                transaction_datetime__date__gte=month,
                transaction_datetime__date__lte=month_end
            ), then=F('amount')),
            output_field=FloatField(),
            default=0
        )), 0.0),
        year_income=Coalesce(Sum(Case(
            When(Q(transaction_type=1, transaction_datetime__gte=year, transaction_datetime__date__lte=today), then=F('amount')),
            output_field=FloatField(),
            default=0
        )), 0.0),
        year_expense=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__gte=year, transaction_datetime__date__lte=today    ), then=F('amount')),
            output_field=FloatField(),
            default=0
        )), 0.0),
        upto_date_income=Coalesce(Sum(Case(
            When(Q(transaction_type=1, transaction_datetime__date__lte=today),
                 then=F('amount')),
            output_field=FloatField(),
            default=0
        )), 0.0),
        upto_date_expense=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__date__lte=today),
                 then=F('amount')),
            output_field=FloatField(),
            default=0
        )), 0.0),
    )
    print(total, month_end, year)
    total_balance = total['total_income'] - total['total_expense']
    data = {
        'username': user.username,
        'total_balance': total_balance
    }
    data.update(total)
    data['today'] = today
    data['today_balance'] = data['today_income'] - data['today_expense']

    data['week'] = week
    data['week_balance'] = data['week_income'] - data['week_expense']

    data['month'] = month
    data['month_balance'] = data['month_income'] - data['month_expense']

    data['year'] = month
    data['year_balance'] = data['year_income'] - data['year_expense']

    data['upto_date_balance'] = data['upto_date_income'] - data['upto_date_expense']

    print(data)
    return render(request, 'home.html', data)


@login_required
def daily(request):
    import datetime
    from datetime import timedelta
    day = request.GET.get('day')
    if day:
        current_day = datetime.datetime.strptime(day, "%Y-%m-%d").date()
    else:
        current_day = datetime.date.today()
    next_day = current_day + timedelta(days=1)
    prev_day = current_day - timedelta(days=1)
    trans = Txn.objects.filter(user=request.user, transaction_type=2, transaction_datetime__date=current_day).order_by('-transaction_datetime')
    data = {
        'trans': trans,
        'current_day': current_day,
        'next_day': next_day,
        'prev_day': prev_day,
        'param_next_day': next_day.__str__(),
        'param_prev_day': prev_day.__str__(),

    }
    print( trans)
    return render(request, 'daily.html', data)

@login_required
def weekly(request):
    import datetime
    from datetime import timedelta
    day = request.GET.get('day')
    if day:
        current_day = datetime.datetime.strptime(day, "%Y-%m-%d").date()
    else:
        current_day = datetime.date.today()

    first_day_of_week = current_day - datetime.timedelta(current_day.weekday())
    last_day_of_week = first_day_of_week + timedelta(days=6)


    weekly_days = {}
    for i in range(7):
        day = first_day_of_week + timedelta(days=i)
        weekly_days[day.__str__()] = Sum(Case(When(Q(transaction_datetime__date=day), then=F('amount')), output_field=FloatField()))
    trans = Txn.objects.filter(user=request.user, transaction_type=2).aggregate(**weekly_days)
    data = {
        'trans': trans,
        'current_day': current_day,
        'first_day_of_week': first_day_of_week,
        'last_day_of_week': last_day_of_week,
        'prev_week': (first_day_of_week - timedelta(days=1)).__str__(),
        'next_week': (last_day_of_week + timedelta(days=1)).__str__(),

    }
    print( data,'------')
    return render(request, 'weekly.html', data)

@login_required
def year_to_date(request):
    user = request.user
    import datetime
    from datetime import timedelta
    today = datetime.date.today()
    week = today - datetime.timedelta(today.weekday())
    month = today.replace(day=1)
    month_end = today.replace(month=week.month + 1, day=1) + timedelta(-1)
    year = today.replace(month=1, day=1)

    monthly = Txn.objects.filter(user=user, transaction_datetime__year=today.year).aggregate(
        January = Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__month=1), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        February=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__month=2), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        March=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__month=3), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        April=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__month=4), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        May=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__month=5), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        June=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__month=6), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        July=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__month=7), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        Augest=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__month=8), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        September=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__month=9), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        October=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__month=10), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        Novermber=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__month=11), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        December=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__month=12), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
    )
    print (monthly)
    return render(request, 'year_to_date.html', {'data': monthly})

@login_required
def this_week(request):
    user = request.user
    import datetime
    from datetime import timedelta
    today = datetime.date.today()
    week = today - datetime.timedelta(today.weekday())
    month = today.replace(day=1)
    month_end = today.replace(month=week.month + 1, day=1) + timedelta(-1)
    year = today.replace(month=1, day=1)
    print (Txn.objects.filter(user=user, transaction_datetime__date__gte=week,
                transaction_datetime__date__lte=today, transaction_datetime__day__lte=5))
    weekly = Txn.objects.filter(user=user, transaction_datetime__date__gte=week,
                transaction_datetime__date__lte=today).aggregate(
        Monday = Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__day=1), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        Tuesday=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__day=2), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        Wednsday=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__day=3), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        Thursday=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__day=4), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        Friday=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__day=5), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        Saturday=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__day=6), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
        Sunday=Coalesce(Sum(Case(
            When(Q(transaction_type=2, transaction_datetime__day=7), then=F('amount')),
            output_field=FloatField(),
            default=0.0
        )), 0.0),
    )
    print (weekly)
    return render(request, 'year_to_date.html', {'data': weekly})
