from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User 

from django.contrib import messages
from django.contrib.messages import constants

from django.contrib import auth #siginifica que posso verifcar o username se existe

# Create your views here.

def cadastro(request):
    if request.method == "GET": # se method http for GET 
        if request.user.is_authenticated: # se user estiver logado vai para raiz 
            return redirect('/')
        return render(request, 'cadastro.html') # se user não estiver logado vai para cadastro 

    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        #nao pode ter um 
    if len(username.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencher todos os Campos')
        return redirect('/auth/cadastro')
        
    user = User.objects.filter(username=username)
    
    if user.exists():
        messages.add_message(request, constants.ERROR, 'Usuário já existe!')
        return redirect('/auth/cadastro')
    
    try:
        user = User.objects.create_user(username=username,
        email=email,
        password=senha)
        user.save()
        messages.add_message(request, constants.SUCCESS, 'Usuário Cadastrado com Sucesso !')
        return redirect('/auth/logar')
    except:
        messages.add_message(request, constants.SUCCESS, 'Erro interno do Sistema.')
        return redirect('/auth/cadastro')


def logar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'logar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        usuario = auth.authenticate(username=username, password=senha)
        if not usuario:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect('/auth/logar')
        else:
            auth.login(request, usuario)
            return redirect('/')

def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')