import codecs
import csv

import pyexcel
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from .models import Product
from .forms import ProductForm
from .tasks import create_products, UserFilter
# Create your views here.
from django_filters.views import FilterView

class ProductListView(FilterView, ListView, CreateView):
    model = Product
    template_name = 'product_list.html'

    def get(self, request, *args, **kwargs):
        context = locals()
        queryset = Product.objects.all()
        paginator = Paginator(queryset, 25)  # Show 25 contacts per page
        page = request.GET.get('page')
        user = request.GET.get('name')
        active = request.GET.get('active')

        context['product_list'] = paginator.get_page(page)
        context['filter'] = UserFilter(request.GET, queryset=queryset)
        if user or active:
            context['product_list'] = UserFilter(request.GET, queryset=queryset).qs

        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            filename = request.FILES['upload_file']
            extension = str(filename).split(".")[-1]
            content = request.FILES['upload_file'].read()

            records = list(pyexcel.get_sheet(file_type=extension, file_content=content))[1:]

            create_products.delay(records)
            messages.success(self.request, 'We are generating your products! Wait a moment and refresh this page.')

            return redirect('assignment:list')

        else:
            product_form = self.form_class

        return render(request, self.template_name )


class ProductCreateView(CreateView, UpdateView):

    model = Product
    queryset = model.objects.all()
    form_class = ProductForm
    template_name = 'product_form.html'

    def get_object(self):
        if self.kwargs.get('pk'):
            return get_object_or_404(self.model,pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if self.kwargs.get('pk'):
                obj = self.model.objects.get(pk=self.kwargs.get('pk'))
                product_form = self.form_class(data=request.POST, instance=obj)
            else:
                product_form = self.form_class(data=request.POST)
            if product_form.is_valid():
                product_form.save()
                return redirect('assignment:list')
            else:
                print(product_form.errors)
        else:
            product_form = self.form_class

        return render(request, self.template_name,
                      {'form': product_form})


def delete(request, pk=None):

    if pk:
        Product.objects.filter(pk=pk).update(active=False)
    else:
        Product.objects.all().delete()
    return redirect('assignment:list')


class ProductDeleteView(CreateView, UpdateView):
    model = Product
    success_url = reverse_lazy("assignment:list")

    def post(self, request, *args, **kwargs):
        registered = False
        if request.method == 'POST':
            if self.kwargs.get('pk'):
                self.model.objects.get(pk=self.kwargs.get('pk')).delete()
            else:
                self.model.objects.all().delete()
            return redirect('assignment:list')
        else:
            product_form = self.form_class

        return render(request, self.template_name,
                      {'form': product_form,
                       'registered': registered})