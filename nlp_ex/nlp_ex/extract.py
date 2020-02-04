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
        keyword_list = HanLP.extractWords(content, 5)
        sentence = '，'.join(sentence_list)
        if len(str(keyword_list)) > 2:
            keyword = str(keyword_list)[1:-1].replace(", ", "、")
        else:
            keyword = "字数过低，无法提取"
        data = {
            'summary': sentence,
            'keyword': keyword
        }
        return JsonResponse(data)
    # ctx = {'summary': sentence_list}
    # return render(request, r"templates\show_pages\text_content.html", ctx)
