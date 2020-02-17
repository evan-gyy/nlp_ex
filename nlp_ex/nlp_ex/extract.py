# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
from django.http import HttpResponse
from django.http import JsonResponse
from pyhanlp import *


def summary(request):
    content = request.POST.get('content')
    if content:
        TextRankSentence = JClass("com.hankcs.hanlp.summary.TextRankSentence")
        sentence_list = HanLP.extractSummary(content, 2)
        keyword = HanLP.extractPhrase(content, 5)
        sentence = str(sentence_list)[1:-1].split(', ')
        keyword_list = str(keyword)[1:-1].split(', ')
        data = {
            'summary': sentence,
            'keyword': keyword_list
        }
        return JsonResponse(data)
    # ctx = {'summary': sentence_list}
    # return render(request, r"templates\show_pages\text_content.html", ctx)
