from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django import forms
from app01 import models
from app01.utils.encrypt import md5

class AdminModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}

    confirm_password = forms.CharField(label='确认密码',widget=forms.PasswordInput())

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password','level']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password'))
        print(password,confirm_password)
        if password != confirm_password:
            raise ValidationError('密码不一致')
        return confirm_password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = models.Admin.objects.exclude(id=self.instance.pk).filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)

def admin_list(request):
    queryset = models.Admin.objects.all()
    return render(request, 'admin_list.html', {'queryset': queryset})

def admin_add(request):
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'admin_add.html', {'form': form,})
    form = AdminModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    """输入校验不过的时候，保留当前页面"""
    return render(request, 'admin_add.html', {'form': form})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')

def admin_edit(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = AdminModelForm(instance=row_object)
        return render(request, 'admin_edit.html', {'form': form})
    form = AdminModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    """输入校验不过的时候，保留当前页面"""
    return render(request, 'admin_edit.html', {'form': form})