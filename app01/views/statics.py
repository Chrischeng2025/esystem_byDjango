from django.shortcuts import render

def statics(request):
    """数据统计页面"""
    return render(request,'statics.html')