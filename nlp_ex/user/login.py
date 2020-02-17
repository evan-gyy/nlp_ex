from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from TestModel.models import UserInfo

def login(request):
    if request.method != "POST":
        return HttpResponse()
    login_state = {}
    user_name = request.POST.get('user_name')
    password = request.POST.get('password')
    user = UserInfo.objects.filter(user_name=user_name, pass_word=password)
    if user:
        user_info = UserInfo.objects.get(user_name=user_name)
        request.session['user_name'] = user_name
        request.session['user_id'] = user_info.user_id
        request.session['is_login'] = True
        login_state['state'] = 1
    else:
        login_state['state'] = 0

    return JsonResponse(login_state)

def logout(request):
    session_key = request.session.session_key
    if session_key:
        request.session.delete(session_key)
        return HttpResponseRedirect("/index")