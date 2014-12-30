from django.shortcuts import render
from fym.models import Trilha, Bloco
from fym.forms import UserForm, UsuarioForm, TrilhaForm, BlocoForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.contrib.auth.models import User

def index(request):
    dicio = {}
    
    dicio['trilhas'] = Trilha.objects.all

    response = render(request, 'fym/index.html', dicio)
    return response

def about(request):

    response = render(request, 'fym/about.html', {})
    return response

def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/fym/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'fym/login.html', {})

def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/fym/')

def add_trilha(request):
    if request.method == 'POST':
        form = TrilhaForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = TrilhaForm()

    return render(request, 'fym/add_trilha.html', {'form': form})

def trilha(request, trilha_slug):
    pre_trilha = Trilha.objects.filter(slug=trilha_slug)
    trilha = pre_trilha[0]
    bloco = Bloco.objects.filter(trilha=trilha.id)
    dicio = {}
    dicio['trilha'] = trilha
    dicio['blocos'] = bloco
    return render(request, 'fym/trilha.html', dicio)

def add_bloco(request, trilha_slug):
    if request.user.is_authenticated():
        user = request.user
    else:
        return index(request)
    form = None
    try:
        trilha = Trilha.objects.get(slug=trilha_slug)
    except Trilha.DoesNotExist:
        trila = None
    dicio = {}
    if request.method == 'POST':
        form = BlocoForm(request.POST)
        if form.is_valid():
            bloco = form.save(commit=False)
            bloco.trilha = trilha
            bloco.usuario = user
            bloco.save()
            return index(request)
        else:
            print form.errors
    else:
        form = BlocoForm()
    dicio['form'] = form
    dicio['slug'] = trilha_slug
    dicio['user'] = user
    return render(request, 'fym/add_bloco.html', dicio)