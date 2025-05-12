from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from app01 import models

def depart_list(request):
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    if request.method == "GET":
        return render(request, 'depart_add.html')
    title = request.POST.get("departmentName")
    models.Department.objects.create(title=title)
    return redirect('/depart/list/')


def depart_delete(request):
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    print("编号为%s的部门删除成功" % nid)
    return redirect('/depart/list/')


def depart_edit(request, nid):
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        print(row_object.title)
        return render(request, 'depart_edit.html', {'title': row_object.title})
    title = request.POST.get("departmentName")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')


def depart_multi(request):
    """批量上传文件"""
    file_object = request.FILES.get('file')
    print(type(file_object))
    return HttpResponse('upload success!')