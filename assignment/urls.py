from django.conf.urls import url
from django.urls import path

from .views import ProductListView, ProductCreateView, ProductDeleteView, delete
from .tasks import create_products, UserFilter
app_name = 'assignment'

urlpatterns = [
    path('list/', ProductListView.as_view(filterset_class=UserFilter,template_name='product_list.html'),name='list'),
    path('add/<int:pk>/', ProductCreateView.as_view(),name='add'),
    path('add/', ProductCreateView.as_view(),name='add'),
    path('remove/',delete, name='remove'),
    path('delete/<int:pk>/',delete,name='delete'),

]
