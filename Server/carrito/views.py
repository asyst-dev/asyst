from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http.response import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
import json
from .models import *
# Create your views here.
@csrf_exempt
def carrito(request):
    if request.method == 'GET':
        if request.GET.get('matricula'):
            if request.GET.get('matricula') == '0':
                return JsonResponse(list(Carrito.objects.all().values()), safe=False)
            encontrado = False
            for carrito in Carrito.objects.all():
                if int(carrito.matricula) == int(request.GET.get('matricula')):
                    encontrado = True
            if not encontrado:
                return HttpResponse('ERROR, matricula invalida')

            matricula = request.GET.get('matricula')
            carr = Carrito.objects.get(matricula=matricula)
            carritodata = model_to_dict(carr)
            try:
                carritodata['rumbo'] = carr.rumbo.ruta
            except:pass
            return JsonResponse(carritodata,safe=False)

        else:
            return HttpResponse('ERROR, ingrese matricula')

    if request.method == 'POST':
        comandos = ('viajando','idavuelta','perdido','reset')
        data = request.body.decode('utf-8').split('-')
        carrito_actual = Carrito.objects.get(matricula=data[0])
        if data[2]=='True':
            data_bool = True
        elif data[2]=='False':
            data_bool = False

        if   data[1]==comandos[0]:carrito_actual.viajando = data_bool
        elif data[1]==comandos[1]:carrito_actual.idavuelta = data_bool
        elif data[1]==comandos[2]:carrito_actual.perdido = data_bool
        elif data[1]==comandos[3]:
            carrito_actual.viajando = False
            carrito_actual.idavuelta = False
            carrito_actual.perdido = False
            carrito_actual.ocupado = False
            carrito_actual.rumbo = None
        carrito_actual.save()
        print(request.body.decode('utf-8'))
        return HttpResponse('OK')
