from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'main/home-page.html')

def faculty_house(request):
    return render(request, 'main/faculty.html')

def ferris_booth(request):
    return render(request, 'main/ferris.html')

def jj_place(request):
    return render(request, 'main/jj.html')

def mike_sub(request):
    return render(request, 'main/mike.html')
