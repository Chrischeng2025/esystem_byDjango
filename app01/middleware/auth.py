from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """如果用户访问的是登录页面，则直接放行"""
        if request.path_info in ['/login/', '/image/code/']:
            return
        """获取当前用户的session信息，如果能获取到，说明已登录，放行"""
        info_dict = request.session.get('info')
        if not info_dict:
            print('用户未登录')
            return redirect('/login/')
        else:
            print('用户已登录',info_dict)
