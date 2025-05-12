from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app01 import models


class UpModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = models.City
        fields = '__all__'


def upload_modelform(request):
    title = 'ModelForm upload'
    if request.method == 'GET':
        form = UpModelForm()
        return render(request,'upload_form.html',{'form':form,'title':title})
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/city/list/')
    return render(request,'upload_form.html',{'form':form,'title':title})


def city_list(request):
    queryset = models.City.objects.all()
    return render(request,'city_list.html',{'queryset':queryset})