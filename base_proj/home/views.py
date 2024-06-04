from django.shortcuts import render

# Create your views here.
from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'home/register.html'
    success_url = 'notes/all'
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes.list')
        return super().get(request, *args, **kwargs)
	

class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'


class LoginInterfaceView(LoginView):
    template_name = 'home/login.html'


class HomeView(TemplateView):
    template_name = 'home/home.html'
    today = date.today()
    today_fmt = today.strftime("%d/%m/%Y")
    extra_content = { 'today': today_fmt }


class InternalTempView(LoginRequiredMixin, TemplateView):
    template_name = 'home/internal.html'
    today = date.today()
    today_fmt = today.strftime("%d/%m/%Y")
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, { 'today': self.today_fmt })
