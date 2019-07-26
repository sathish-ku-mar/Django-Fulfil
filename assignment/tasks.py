import string

from .models import Product

from celery import shared_task

@shared_task
def create_products(records):
    for record in records:
        product = Product(name=record[0], sku=record[1], description=record[2])
        try:
            product.save()
        except:
            # if the're a problem anywhere, you wanna know about it
            print("there was a problem with line")
    return '{} products created with success!'.format(len(records))




import django_filters

class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['name', ]