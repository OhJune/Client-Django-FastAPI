from django.shortcuts import render
from .models import board
from .forms import boardForm
def index(request):
    return render(request, 'main_site/index.html')

def page1(request):
    return render(request, 'main_site/page1.html')

def page2(request):
    return render(request, 'main_site/page2.html')

def page3(request):
    if request.method == 'POST':
        form = boardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.create_date = timezone.now()
            board.save()
            return redirect('main_site:index')
    else:
        form = boardForm(request)
    context = {'form': form}
    return render(request, 'main_site/page3.html',context)

def page4(request):
    return render(request, 'main_site/page4.html')

def about(request):
    return render(request, 'main_site/about.html')

def contact(request):
    return render(request, 'main_site/contact.html')