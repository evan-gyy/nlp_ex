# -*- coding: utf-8 -*-
from django.http import HttpResponse

from TestModel.models import NLP

# 数据库操作
def testdb(request):
    # initial
    response = ""
    response1 = ""

    # get all rows
    list = NLP.objects.all()

    # filter = WHERE
    response2 = NLP.objects.filter(id=1)
    # get one of them
    response3 = NLP.objects.get(id=1)
    # order
    NLP.objects.order_by("id")
    # together
    NLP.objects.filter(name="runoob").order_by("id")
    # output
    for var in list:
        response1 += var.name + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")