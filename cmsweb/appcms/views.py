from django.shortcuts import render

# Create your views here.

# myapp/views.py

def mi_vista(request):
    return render(request, 'socialaccount/login.html')