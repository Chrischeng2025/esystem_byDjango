from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django import forms
from app01 import models

def pretty_list(request):
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict['mobile__contains'] = search_data
    queryset = models.PrettyNum.objects.filter(**data_dict)
    print(queryset)
    return render(request, 'pretty_list.html', {'queryset': queryset, 'search_data': search_data})


class PrettyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}

    mobile = forms.CharField(label="手机号", validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')])

    class Meta:
        model = models.PrettyNum
        fields = '__all__'

    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile


def pretty_add(request):
    if request.method == "GET":
        form = PrettyForm()
        return render(request, 'pretty_add.html', {'form': form})
    form = PrettyForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    """输入校验不过的时候，保留当前页面"""
    return render(request, 'pretty_add.html', {'form': form})


def pretty_edit(request, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyForm(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})
    form = PrettyForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    """输入校验不过的时候，保留当前页面"""
    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
