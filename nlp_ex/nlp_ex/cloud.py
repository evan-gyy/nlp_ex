# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf

def get_cloud(request):
    ctx = {}
    if request.POST:
        ctx['cloud'] = request.POST['q']
    return render(request, r"templates\show_pages\text_title.html", ctx)