from django.shortcuts import render

# Protección de vistas con login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView

@login_required
def home(request):
    return render(request, 'dashboard/index.html')

class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'