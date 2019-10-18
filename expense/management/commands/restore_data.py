import csv

from django.core.management.base import BaseCommand
from expense.models import MainCategory, SubCategory, Transaction
import datetime
class Command(BaseCommand):

    def handle(self, *args, **options):


        """
        Algo:

        :param options:
        :return:
        """
        print("started...")
        user_id = 11
        with open('../expensemanager18oct.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # print(row)
                
                try:
                    amount = float(row[None][1])
                except:
                    print(row[None][1], '++++')
                    continue
                main_category, f = MainCategory.objects.get_or_create(name=row[None][2], user_id=user_id)
                sub_category, f = SubCategory.objects.get_or_create(name=row[None][3], user_id=user_id, category=main_category)

                samayam = '{} 14:00'.format(row[None][0])
                txn_time = datetime.datetime.strptime(samayam, '%Y-%m-%d %H:%M')
                Transaction.objects.create(
                    user_id=user_id,
                    main_category = main_category,
                    sub_category = sub_category,
                    transaction_type = 2 if amount < 0 else 1,
                    amount = abs(amount),
                    payee = row[None][7],
                    transaction_datetime = txn_time
                )


        print('completed...')
