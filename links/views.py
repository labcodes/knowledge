from django.shortcuts import render
from .models import Link

# Create your views here.


def index(request):
    links = Link.objects.all()
    return render(request, 'links/index.html', {'links': links})
