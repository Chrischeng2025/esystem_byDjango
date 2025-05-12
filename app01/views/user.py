from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django import forms
from app01 import models

def user_list(request):
    queryset = models.UserInfo.objects.all()
    return render(request, 'user_list.html', {'queryset': queryset})


class MyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = models.UserInfo
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
            'create_time': forms.DateInput(attrs={'type': 'date'})
        }

def user_add(request):
    if request.method == "GET":
        form = MyForm()
        return render(request, 'user_add.html', {'form': form})
    form = MyForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    """输入校验不过的时候，保留当前页面"""
    return render(request, 'user_add.html', {'form': form})

def user_edit(request, nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = MyForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})
    form = MyForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    """输入校验不过的时候，保留当前页面"""
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')