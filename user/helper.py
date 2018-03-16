from django.shortcuts import render, redirect

from user.models import User, UserPermission, Permission


def check_perm(need_perm):
    def wrap1(view_func):
        def wrap2(request, *args, **kwargs):
            uid = request.session.get('uid')
            if uid is not None:
                user = User.objects.get(id=uid)
                if user.perm >= need_perm:
                    return view_func(request, *args, **kwargs)
                else:
                    return render(request, 'blockers.html')
            else:
                return redirect('/user/login/')
        return wrap2
    return wrap1


def check_perm2(need_perm):
    def wrap1(func):
        def wrap2(request, *args, **kwargs):
            uid = request.session.get('uid')
            if uid:
                user = User.objects.get(id=uid)
                perm_names = user.perms
                if need_perm in perm_names:
                    return func(request, *args, **kwargs)
                else:
                    return render(request, 'blockers.html')
            return redirect('/user/login/')
        return wrap2
    return wrap1
