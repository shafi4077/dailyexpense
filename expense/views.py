from django.http.response import JsonResponse
# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from expense.models import MainCategory, Transaction, SubCategory
from .forms import AddTransactionForm


def categories(request):
    data = [
        {
            'category': category.name,
            'sub_categories': [
                {
                    'id': s.id,
                    'name': s.name
                } for s in category.subcategory_set.all()
            ]
        } for category in MainCategory.objects.filter(user=request.user)

    ]
    print(data, request.user.id)
    return JsonResponse(data, safe=False)


class AddTransaction(View):
    def post(self, request):
        data = request.POST
        print(data)
        import datetime
        form = AddTransactionForm(data=data)
        print (form.data)
        if form.is_valid():
            sub_category = SubCategory.objects.get(id=data['category_id'])
            Transaction.objects.create(
                user=request.user,
                transaction_type=data['transaction_type'],
                main_category_id=sub_category.category_id,
                sub_category=sub_category,
                amount=data['amount'],
                payee=data.get('payee'),
                transaction_datetime=datetime.datetime.strptime(data['created_at'], '%d/%m/%Y %H:%M')
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Added'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': form.errors
            })

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(AddTransaction, self).dispatch(*args, **kwargs)
