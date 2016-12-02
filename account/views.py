from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Autenticación Satisfactoria")
                else:
                    return HttpResponse("Cuenta Deshabilitada")
            else:
                return HttpResponse("Login Invalido")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})

@login_required
def dashboard(request):
    section = "dashboard"
    return render(request, 'account/dashboard.html', {'section':section})

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #Creamos un nuevo objecto "Usuario" que aún no sera almacenado
            new_user = user_form.save(commit=False)
            #Escogemos la contraseña seleccionada
            new_user.set_password(user_form.cleaned_data['password'])
            #Guardamos el objecto Usuario
            new_user.save()
            #Retornamos el template al ser el registro exitoso
            return render(request, 'registration/register_done.html', {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,  'registration/register.html', {'user_form':user_form})
