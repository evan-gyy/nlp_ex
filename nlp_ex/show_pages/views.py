from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'templates/show_pages/index.html')

def text_title(request):
    return render(request, 'templates/show_pages/text_title.html')

def text_content(request):
    return render(request, 'templates/show_pages/text_content.html')

def spread_wci(request):
    return render(request, 'templates/show_pages/spread_wci.html')