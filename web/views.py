from django.shortcuts import render

# Create your views here.
def home(request):
    """
    Página principal pública.
    """
    return render(request, "web/home.html")
