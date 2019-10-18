from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from expense.models import MainCategory, SubCategory


@receiver(post_save, sender=User)
def add_defaul_categories_to_user(sender, instance, created, **kwargs):
    print(sender, ' -------', instance)
    if created:
        for category in MainCategory.objects.filter(is_default=True):
            main_category = MainCategory.objects.create(user=instance, name=category.name)
            for sub_category in category.subcategory_set.all():
                SubCategory.objects.create(user=instance, name=sub_category.name, category=main_category)


