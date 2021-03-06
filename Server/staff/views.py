from django.db.models.expressions import F
from django.shortcuts import redirect, render
from django.utils.html import escapejs
from main.models import Activo, Stock,Peticion
from django.http import JsonResponse
from django.http.response import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
import json
from carrito.models import Carrito

@staff_member_required(login_url='home')
def staffHome(request):
    return redirect('pedidos')

# ------------------------------------------------------- PEDIDOS -----------------------------------
@staff_member_required(login_url='home')
def pedidos(request):
    pendientesDb = Peticion.objects.filter(estado = 1)
    pendientes = JsonResponse(list(pendientesDb.values()),safe=False)
    for i in pendientes: pendientes = i.decode('utf-8')
    usuarioDb = get_user_model()
    usuariosDb = usuarioDb.objects.filter(is_staff=False)
    usuariosDbTemp = list(usuariosDb.values())
    for i in usuariosDbTemp:
        del i['password']
        del i['email']
    usuarios = JsonResponse(usuariosDbTemp,safe=False)
    for i in usuarios: usuarios = i.decode('utf-8')
    carritosDb = Carrito.objects.all()
    carritos = JsonResponse(list(carritosDb.values()),safe=False)
    for i in carritos: carritos = i.decode('utf-8')
    context = {'pendientes':pendientes,'usuarios':usuarios,'carritos':carritos}
    if request.method == 'POST':
        '''
        req = json.loads(request.body.decode('utf-8'))
        print(req)
        pedido = Peticion.objects.get(id=req['id'])
        pedido.mensaje = req['msg']
        pedido.estado  = req['estado']
        pedido.staff   = request.user
        pedido.save()
        '''
        context['post'] = True
        print(request.body)
        print(f'ID= {request.POST.get("id")}')
        print(f'STATUS= {request.POST.get("status")}')
        print(f'MSG= {request.POST.get("msg")}')
        # agarro los carritos libres
        carritosLibres = Carrito.objects.filter(ocupado=False)
        vacio = False
        if len(carritosLibres) == 0: vacio = True

        if (int(request.POST.get('status'))==2 and vacio):
            print('ERROR, Aprobacion sin flota')
            context['matricula'] = 0
            context['reject'] = False
            return render(request,'Staff-pedidos.html',context=context)
        else:
            # print(carritosLibres[0])
            pedido = Peticion.objects.get(id=request.POST.get('id'))
            if pedido.estado != 1:
                print('ERROR, modificando no pendiente','-'*20)
                return redirect('pedidos')
            pedido.mensaje = request.POST.get('msg')
            pedido.estado = request.POST.get('status')
            pedido.staff = request.user
            pedido.save()
            if int(request.POST.get('status')) == 2:
                carritosLibres[0].ocupado = True
                carritosLibres[0].rumbo = pedido.destino
                context['matricula'] = carritosLibres[0].matricula
                activo = Activo.objects.get(usuario=pedido.autor)
                activo.carrito = carritosLibres[0]
                activo.save()
                carritosLibres[0].save()
                context['reject'] = False
                return render(request,'Staff-pedidos.html',context=context)

            elif int(request.POST.get('status')==3):
                context['matricula'] = 0
                context['reject'] = True
                return render(request,'Staff-pedidos.html',context=context)
        # print(context['matricula'])
    return render(request,'Staff-pedidos.html',context=context)


#--------------------------------------------STOCK---------------------------------------------------
@staff_member_required(login_url='home')
def stock(request):
    if request.method =='GET':
        stockDb = Stock.objects.all()
        stock = JsonResponse(list(stockDb.values()),safe=False)
        for i in stock: stock = i.decode('utf-8')
        return render(request,'Staff-stock.html',context={'stock':stock})

@staff_member_required(login_url='home')
def addStock(request):
    if request.method == 'POST':
        # print(request.body)
        req = json.loads(request.body.decode('utf-8'))
        print(req)
        stock = Stock(
            nombre= req['nombre'],
            cantidad= req['cantidad'],
            clase= req['clase']
        )
        stock.save()
    return redirect('stock')

@staff_member_required(login_url='home')
def editStock(request,id):
    if request.method == 'POST':
        # print(request.body)
        req = json.loads(request.body.decode('utf-8'))
        edited = Stock.objects.get(id=id)
        print(req)
        edited.nombre = req['nombre']
        edited.clase = req['clase']
        edited.cantidad = req['cantidad']
        edited.save()
    return redirect('stock')

@staff_member_required(login_url='home')
def removeStock(request, id):
    dato = Stock.objects.get(id=id)
    dato.delete()
    return redirect('stock')

# ----------------------------------------------------REGISTROS------------------------------------
@staff_member_required(login_url='home')
def registros(request):
    peticionesDb = Peticion.objects.exclude(estado = 1)
    peticiones = JsonResponse(list(peticionesDb.values())[::-1],safe=False)
    for i in peticiones: peticiones = i.decode('utf-8')
    usuarioDb = get_user_model()
    usuariosDb = usuarioDb.objects.all()
    usuariosDbTemp = list(usuariosDb.values())
    for i in usuariosDbTemp:
        del i['password']
    usuarios = JsonResponse(usuariosDbTemp,safe=False)
    for i in usuarios: usuarios = i.decode('utf-8')

    return render(request,'Staff-registros.html',context={'peticiones':peticiones,'usuarios':usuarios})
