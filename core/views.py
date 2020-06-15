from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse


def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('Usuário')
        password = request.POST.get('Senha')
        user = authenticate(username=username, password=password)
        if user is not None:
            login (request,user)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou Senha inválido")
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=2)
    evento = Evento.objects.filter(usuario = usuario,
                                   data_evento__gt = data_atual)
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        hora_evento = request.POST.get('hora_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        local = request.POST.get('locale')
        id_evento = request.POST.get('id_evento')

        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.data_evento = data_evento+ ' ' + hora_evento
                evento.descricao = descricao
                evento.localidade = local
                evento.save()
            # Evento.objects.filter(id=id_evento).update(titulo= titulo,
            #                                            data_evento = data_evento + ' ' + hora_evento,
            #                                            descricao = descricao,
            #                                            localidade = local)
        else:
            Evento.objects.create(titulo = titulo,
                                  data_evento = data_evento + ' ' + hora_evento,
                                  descricao = descricao,
                                  usuario = usuario,
                                  localidade = local)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise  Http404()

    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')


def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id','titulo')
    return JsonResponse(list(evento), safe=False)