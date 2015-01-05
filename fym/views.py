from django.shortcuts import render
from fym.models import Trilha, Bloco, Usuario
from fym.forms import UserForm, UsuarioForm, TrilhaForm, BlocoForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.contrib.auth.models import User

def index(request):
    dicio = {}
    dicio['trilhas'] = Trilha.objects.order_by('-id')[:8]
    if request.user.is_authenticated():
        user = request.user
        dicio['usuario'] = Usuario.objects.get(user=user)
    response = render(request, 'fym/index.html', dicio)
    return response

def about(request):
    dicio = {}
    if request.user.is_authenticated():
        user = request.user
        dicio['usuario'] = Usuario.objects.get(user=user)
    
    response = render(request, 'fym/about.html', dicio)
    return response

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/fym/')
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
    dicio = {}
    if request.user.is_authenticated():
        user = request.user
        dicio['usuario'] = Usuario.objects.get(user=user)
    else:
        return HttpResponseRedirect('/fym/')

    if request.method == 'POST':
        form1 = TrilhaForm(request.POST)
        form2 = BlocoForm(request.POST)
        if form1.is_valid():
            trilha = form1.save(commit=True)
            if form2.is_valid():
                bloco = form2.save(commit=False)
                bloco.trilha = trilha
                bloco.usuario = user
                bloco.save()
                return index(request)
            else:
                print form2.errors
        else:
            print form1.errors
    else:
        form1 = TrilhaForm()
        form2 = BlocoForm()

    dicio['form1'] = form1
    dicio['form2'] = form2   
    return render(request, 'fym/add_trilha.html', dicio)

def trilha(request, trilha_slug):
    dicio = {}
    if request.user.is_authenticated():
        user = request.user
        dicio['usuario'] = Usuario.objects.get(user=user)

    pre_trilha = Trilha.objects.filter(slug=trilha_slug)
    trilha = pre_trilha[0]
    bloco = Bloco.objects.filter(trilha=trilha.id)
    dicio['trilha'] = trilha
    dicio['blocos'] = bloco
    dicio['slug'] = trilha_slug
    return render(request, 'fym/trilha.html', dicio)

def trilhas(request):
    dicio = {}
    if request.user.is_authenticated():
        user = request.user
        dicio['usuario'] = Usuario.objects.get(user=user)

    trilhas = Trilha.objects.all()
    dicio['trilhas'] = trilhas
    return render(request, 'fym/trilhas.html', dicio)

def add_bloco(request, trilha_slug):
    dicio = {}
    if request.user.is_authenticated():
        user = request.user
        dicio['usuario'] = Usuario.objects.get(user=user)
    else:
        return index(request)
    form = None
    try:
        trilha = Trilha.objects.get(slug=trilha_slug)
    except Trilha.DoesNotExist:
        trila = None
    if request.method == 'POST':
        form = BlocoForm(request.POST)
        if form.is_valid():
            bloco = form.save(commit=False)
            bloco.trilha = trilha
            bloco.usuario = user
            bloco.save()
            return HttpResponseRedirect('/fym/')
        else:
            print form.errors
    else:
        form = BlocoForm()
    dicio['form'] = form
    dicio['slug'] = trilha_slug
    dicio['user'] = user
    return render(request, 'fym/add_bloco.html', dicio)

def signup(request):
    dicio = {}
    if request.user.is_authenticated():
        return HttpResponseRedirect('/fym/')

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        usuario_form = UsuarioForm(data=request.POST)

        if user_form.is_valid() and usuario_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            usuario = usuario_form.save(commit=False)
            usuario.user = user
            usuario.save()
            registered = True
            return HttpResponseRedirect('/fym/')

        else:
            print user_form.errors, usuario_form.errors
    else:
        user_form = UserForm()
        usuario_form = UsuarioForm()

    dicio['user_form'] = user_form
    dicio['usuario_form'] = usuario_form
    dicio['registered'] = registered
    return render(request, 'fym/signup.html', dicio)

def meus_blocos(request):
    dicio = {}
    if request.user.is_authenticated():
        user = request.user
        dicio['usuario'] = Usuario.objects.get(user=user)
    else:
        return HttpResponseRedirect('/fym/')

    blocos = Bloco.objects.filter(usuario=user)
    dicio['blocos'] = blocos
    return render(request, 'fym/meus_blocos.html', dicio)

