from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from app01 import models
from app01.utils.captcha import generate_captcha
from PIL import Image, ImageDraw, ImageFont
import random
import string

class LoginForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = models.Admin
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }



def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request.POST)
    """校验用户名和密码"""
    if form.is_valid():
        """校验成功，跳转页面"""
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        admin_object = models.Admin.objects.filter(username=username, password=password).first()
        if not admin_object:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})
        #生成随机字符串，写入用户cookie并生成session
        request.session['info'] = {'id': admin_object.id, 'username': admin_object.username}
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('/admin/list/')

def logout(request):
    request.session.clear()
    return redirect('/login/')

def image_code(request):
    """生成图片验证码"""
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    captcha_image = generate_captcha(captcha_text)
    buffer=BytesIO()
    captcha_image.save(buffer,'png')
    image_data = buffer.getvalue()

    return HttpResponse(image_data, content_type='image/png')
