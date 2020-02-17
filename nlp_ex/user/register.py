from django.http import JsonResponse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from TestModel.models import UserInfo
from django.utils import timezone
from random import *

# 生成随机字符串
def get_random_str(random_str_length=64):
    strings = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_str_length):
        strings += chars[random.randint(0, length)]
    return strings

# 注册
def register(request):
    if request.method != "POST":
        return HttpResponse()
    register_state = {}
    user_name = request.POST.get('user_name')
    password = request.POST.get('password')
    try:
        UserInfo.objects.get(user_name=user_name)
        register_state['state'] = 0
    except ObjectDoesNotExist:
        if UserInfo.objects.last() is None:
            user_id = 1
        else:
            user_id = UserInfo.objects.last().user_id + 1
        UserInfo.objects.create(user_name=user_name, user_id=user_id, pass_word=password, user_token=get_random_str(64), token_last_modified=timezone.now())
        register_state['state'] = 1
    except KeyError:
        register_state['state'] = 2

    return JsonResponse(register_state)