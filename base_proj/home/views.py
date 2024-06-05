from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, render


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'home/signup.html'
    success_url = 'home'
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        response = super().form_valid(form)
        # Here, we log in the user
        login(self.request, self.object)
        return response
	

class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'


class LoginInterfaceView(LoginView):
    template_name = 'home/login.html'
    success_url = 'home'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = 'home/home.html'
    today = date.today()
    today_fmt = today.strftime("%d/%m/%Y")
    extra_content = { 'today': today_fmt }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_content)
        return context


class InternalTempView(LoginRequiredMixin, TemplateView):
    template_name = 'home/internal.html'
    today = date.today()
    today_fmt = today.strftime("%d/%m/%Y")
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, { 'today': self.today_fmt })
