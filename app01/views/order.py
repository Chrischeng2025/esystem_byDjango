from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from app01 import models



class OrderModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = models.Order
        fields = "__all__"

def order_list(request):
    form = OrderModelForm()
    return render(request, 'order_list.html', {'form': form})

@csrf_exempt
def order_add(request):
    """新建订单Ajax请求"""
    form = OrderModelForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})


