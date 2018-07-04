from django.contrib.auth.decorators import login_required
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from .numeroaletra import to_word
from reportlab.lib import colors
from django.views import View
from venta.models import *
from venta.tables import *
from io import BytesIO
from entrada.models import *
from salida.models import *
from produccion.models import *
from produccion.tables import ProductoProduccionTable
from .form import *
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
import os.path
from django.db.models import Count, Sum


datos = {   'razon_social': 'Grupo Barismo S de RL de CV',
            'rfc' : 'GBA160112QQ6',
            'direccion' : 'Playa Hemosillo #104 Col. San Pablo Comevi',
            'cp' : '76125',
            'ciudad' : 'Queretaro',
            'estado' : 'Queretaro',
            'telefono' : '2-35-42-37',
            'correo' : 'contacto@barismoallimite.com.mx',
            }

@login_required(login_url='/admin/login/')
def reporteventa(request, pk):
    venta = Venta.objects.get(pk=pk)
    productoventas = ProductoVenta.objects.filter(venta__pk=pk)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="H' + venta.referencia() +'.pdf"'

    # Create the PDF object, using the BytesIO object as its "file."
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize = letter)

    #Ancho=612 y alto=792 de la página
    ancho, alto = letter

    #informacion de la empresa
    c.setFont("Helvetica", 30)
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo-barismo1.jpg')
    c.drawImage(fn, 50, 680, width=220, height=90)
    c.setFont("Helvetica", 8)
    c.drawString(250, 745, datos['razon_social'])
    c.drawString(250, 735, datos['rfc'])
    c.drawString(250, 725, datos['direccion'] + " CP:" + datos['cp'])
    c.drawString(250, 715, datos['ciudad'] + ", " + datos['estado'])
    c.drawString(250, 705, datos['telefono'] + "  " + datos['correo'])

    #Datos de la cotizacion
    c.setFont("Helvetica", 10)
    d = [['   VENTA N°   '], [venta.referencia()],
         ['FECHA'], [venta.fecha_creacion],
         ['FACTURA'], [venta.no_de_factura],
         ['ESTADO'], [venta.pago()]]

    table=Table(d)
    table.setStyle(TableStyle([ ('ALIGN',(0,0),(-1,-1),'CENTER'),
                                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('BOX',(0,0),(-1,-1),2,colors.black),
                                ('BACKGROUND', (0, 0), (0, 0), colors.lavender),
                                ('BACKGROUND', (0, 2), (0, 2), colors.lavender),
                                ('BACKGROUND', (0, 4), (0, 4), colors.lavender),
                                ('BACKGROUND', (0, -2), (0, -2), colors.lavender),]))

    #Importe con letra
    table.wrapOn(c, 20, 50)
    table.drawOn(c,495,620)

    #Datos del cliente
    c.setFont("Helvetica", 10)
    c.drawString(55, 660, "CLIENTE:" + venta.cliente.contacto)
    c.drawString(55, 645, "RAZON SOCIAL:" + venta.cliente.razon_social)
    c.drawString(55, 630, "RFC:" + venta.cliente.rfc)
    c.drawString(55, 615, "DIRECCION:" + venta.cliente.direccion + ' ' + venta.cliente.ciudad + " CP:" + venta.cliente.codigo_postal)

    #Conceptos
    data= [['CANTIDAD', 'DESCRIPCION', 'PRECIOU', 'PRECIO TOTAL'],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', '', ''],
     ['', '', 'SUBTOTAL', ''],
     ['', '', 'IVA', ''],
     ['', '', 'TOTAL', '']
     ]

    j = 1
    sub = 0
    total = 0
    for i in productoventas:
        cantidad = i.cantidad
        precio = i.producto.precio_de_venta
        total = cantidad * precio
        data[j][0] = cantidad
        data[j][1] = i.producto.codigo_de_barras + ' ' + i.producto.producto
        data[j][2] = precio
        data[j][3] = format(total, '.2f')
        sub += total
        j += 1

    data[26][3] = "$" +  format(sub, '.2f')
    if venta.iva > 0:
        data[27][3] = "$" + format(sub * venta.iva / 100, '.2f')
    else:
        data[27][3] = "$0.00"
    data[28][3] = "$" + str(venta.total)


    t=Table(data,colWidths=[60,310,58,86])
    t.setStyle(TableStyle([ ('ALIGN',(0,1),(0,-1),'CENTER'),
                            ('ALIGN',(2,1),(2,-4),'CENTER'),
                            ('ALIGN',(3,1),(3,-1),'CENTER'),
                            ('BOX',(0,0),(-1,-4),2,colors.black),
                            ('BOX',(0,0),(4,0),2,colors.black),
                            ('INNERGRID', (-2,-3), (-1,-1), 0.25, colors.black),
                            ('BOX',(-2,-3),(-1,-1),2,colors.black),
                            ('BOX',(-1,-3),(-1,-1),2,colors.black),
                            ('BOX',(0,-3),(-2,-1),2,colors.black),
                            ('BACKGROUND', (0, 0), (-1, 0), colors.lavender),
                            ('BACKGROUND', (-2, -3), (-2, -1), colors.lavender),
                            ('LINEAFTER',(0,0),(0,-4),1,colors.black),
                            ('LINEAFTER',(1,0),(1,-4),1,colors.black),
                            ('LINEAFTER',(2,0),(2,-4),1,colors.black),
                        ]))
    #Importe con letra
    c.drawString(60, 95, "TOTAL CON LETRA:")
    decimales = int((float(venta.total) - int(venta.total)) * 100)
    c.drawString(60, 73, to_word(total) + ' PESOS ' + '%02d' % int(decimales) + '/100' + ' MN')

    t.wrapOn(c, 20, 50)
    t.drawOn(c,55,55)

    c.showPage()
    c.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required(login_url='/admin/login/')
def reporteentrada(request,pk):
    #definimos los modelos para el reporte
    entrada = Entrada.objects.get(pk=pk)
    productoentrada = ProductoEntrada.objects.filter(entrada__pk=pk)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="H' + entrada.referencia() +'.pdf"'

    # Create the PDF object, using the BytesIO object as its "file."
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize = letter)

    #Definimos la fuente que vamos a utilizar
    c.setFont("Helvetica", 12)

    data = [['Reporte de entrada ' + entrada.referencia()],
        ['Fecha de creacion: ' + str(entrada.fecha_creacion)]]

    tabla=Table(data,colWidths=[612])
    tabla.setStyle(TableStyle([ ('ALIGN',(0,0),(0,-1),'CENTER'),
                        ]))

    tabla.wrapOn(c, 0, 0)
    tabla.drawOn(c,0,730)


    #Conceptos
    data= [['CODIGO', 'DESCRIPCION', 'CANTIDAD']]
    for i in range(37):
        data.append(['', '', ''])

    j = 1
    for i in productoentrada:
        data[j][0] = i.producto.codigo_de_barras
        data[j][1] = i.producto
        data[j][2] = i.cantidad
        j += 1

    t=Table(data,colWidths=[60,386,68])
    t.setStyle(TableStyle([ ('ALIGN',(0,1),(0,-1),'CENTER'),
                            ('ALIGN',(2,1),(2,-4),'CENTER'),
                            ('ALIGN',(2,1),(2,-1),'CENTER'),
                            ('BOX',(0,0),(-1,-1),2,colors.black),
                            ('BOX',(0,0),(3,0),2,colors.black),
                            ('LINEAFTER',(0,0),(0,-1),1,colors.black),
                            ('LINEAFTER',(1,0),(1,-1),1,colors.black),
                            ('LINEAFTER',(2,0),(2,-1),1,colors.black),
                        ]))
    #Importe con letra
    t.wrapOn(c, 20, 50)
    t.drawOn(c,50,35)



    c.showPage()
    c.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required(login_url='/admin/login/')
def reportesalida(request,pk):
    #definimos los modelos para el reporte
    salida = Salida.objects.get(pk=pk)
    productosalida = ProductoSalida.objects.filter(salida__pk=pk)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="H' + salida.referencia() +'.pdf"'

    # Create the PDF object, using the BytesIO object as its "file."
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize = letter)

    #Definimos la fuente que vamos a utilizar
    c.setFont("Helvetica", 12)

    data = [['Reporte de entrada ' + salida.referencia()],
        ['Fecha de creacion: ' + str(salida.fecha_creacion)]]

    tabla=Table(data,colWidths=[612])
    tabla.setStyle(TableStyle([ ('ALIGN',(0,0),(0,-1),'CENTER'),
                        ]))

    tabla.wrapOn(c, 0, 0)
    tabla.drawOn(c,0,730)


    #Conceptos
    data= [['CODIGO', 'DESCRIPCION', 'CANTIDAD']]
    for i in range(37):
        data.append(['', '', ''])

    j = 1
    for i in productosalida:
        data[j][0] = i.producto.codigo_de_barras
        data[j][1] = i.producto
        data[j][2] = i.cantidad
        j += 1

    t=Table(data,colWidths=[60,386,68])
    t.setStyle(TableStyle([ ('ALIGN',(0,1),(0,-1),'CENTER'),
                            ('ALIGN',(2,1),(2,-4),'CENTER'),
                            ('ALIGN',(2,1),(2,-1),'CENTER'),
                            ('BOX',(0,0),(-1,-1),2,colors.black),
                            ('BOX',(0,0),(3,0),2,colors.black),
                            ('LINEAFTER',(0,0),(0,-1),1,colors.black),
                            ('LINEAFTER',(1,0),(1,-1),1,colors.black),
                            ('LINEAFTER',(2,0),(2,-1),1,colors.black),
                        ]))
    #Importe con letra
    t.wrapOn(c, 20, 50)
    t.drawOn(c,50,35)



    c.showPage()
    c.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required(login_url='/admin/login/')
def reporteproduccion(request,pk):
    #definimos los modelos para el reporte
    salida = Produccion.objects.get(pk=pk)
    productosalida = ProductoProduccion.objects.filter(produccion__pk=pk)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="H' + salida.referencia() +'.pdf"'

    # Create the PDF object, using the BytesIO object as its "file."
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize = letter)

    #Definimos la fuente que vamos a utilizar
    c.setFont("Helvetica", 12)

    data = [['Reporte de entrada ' + salida.referencia()],
        ['Fecha de creacion: ' + str(salida.fecha_creacion)]]

    tabla=Table(data,colWidths=[612])
    tabla.setStyle(TableStyle([ ('ALIGN',(0,0),(0,-1),'CENTER'),
                        ]))

    tabla.wrapOn(c, 0, 0)
    tabla.drawOn(c,0,730)


    #Conceptos
    data= [['PRODUCTO A PRODUCIR', 'CANTIDAD', 'PRODUCTO PRODUCIDO', 'CANTIDAD']]
    for i in range(37):
        data.append(['', '', '', ''])

    j = 1
    for i in productosalida:
        data[j][0] = i.producto_para_producir.codigo_de_barras + ' ' + i.producto_para_producir.producto
        data[j][1] = i.cantidad_para_producir
        data[j][2] = i.producto_producido.codigo_de_barras + ' ' + i.producto_producido.producto
        data[j][3] = i.cantidad_producido
        j += 1

    t=Table(data,colWidths=[195,60,195,60])
    t.setStyle(TableStyle([ ('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('BOX',(0,0),(-1,-1),2,colors.black),
                            ('BOX',(0,0),(3,0),2,colors.black),
                            ('LINEAFTER',(0,0),(0,-1),1,colors.black),
                            ('LINEAFTER',(1,0),(1,-1),1,colors.black),
                            ('LINEAFTER',(2,0),(2,-1),1,colors.black),
                            ('LINEAFTER',(2,0),(2,-1),1,colors.black),
                        ]))
    #Importe con letra
    t.wrapOn(c, 20, 50)
    t.drawOn(c,50,35)



    c.showPage()
    c.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def reporte(request, mes = '1', año = '2018'):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReporteForm(request.POST)
        año = request.POST['mes']
        mes = request.POST['año']
        return HttpResponseRedirect(reverse_lazy('reporte_mes', args = (año, mes)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReporteForm(initial = {'mes':1 , 'año': 2018})

    return render(request, 'crear.html', {'form': form})

class ReporteMesView(TemplateView):
    template_name = "reporte.html"
    mes_choise = {'1' : 'Enero',
                  '2' : 'Febrero',
                  '3' :'Marzo',
                  '4' : 'Abril',
                  '5' : 'Mayo',
                  '6' : 'Junio',
                  '7' : 'Julio',
                  '8' : 'Agosto',
                  '9' : 'Septiembre',
                  '10' : 'Octubre',
                  '11' : 'Noviembre',
                  '12' : 'Diciembre'}
    def comprobarventa(self, mes , año):
        self.ventas = Venta.objects.filter(fecha_creacion__year = año).filter(fecha_creacion__month = mes)
        if self.ventas:
            return True
        else:
            return False

    def comprobarproduccion(self, mes , año):
        self.produccion = Produccion.objects.filter(fecha_creacion__year = año).filter(fecha_creacion__month = mes)
        self.productoproduccion = ProductoProduccion.objects.filter(produccion__fecha_creacion__year = año).filter(produccion__fecha_creacion__month = mes)
        self.verde = self.productoproduccion.aggregate(total=Sum('cantidad_para_producir'))['total']
        self.tostado = self.productoproduccion.aggregate(total=Sum('cantidad_producido'))['total']
        if self.produccion and self.productoproduccion:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mes = kwargs.get('mes')
        año = kwargs.get('año')
        context['mes'] = self.mes_choise.get(mes)
        context['año'] = año
        if self.comprobarventa(mes,año) == True:
            context['existeventas'] = True
            context['cantidad'] = len(self.ventas)
            context['tableventas'] = VentaTable(self.ventas)
            context['pagado'] = self.ventas.aggregate(total=Sum('a_cuenta'))['total']
            context['no_pagado'] = self.ventas.aggregate(total=Sum('falta'))['total']
            context['total'] = self.ventas.aggregate(total=Sum('total'))['total']
        else:
            context['existeventas'] = False

        if self.comprobarproduccion(mes,año) == True:
            context['existeproduccion'] = True
            context['cantidadproduccion'] = len(self.produccion)
            context['verde'] = self.verde
            context['tostado'] = self.tostado
            context['tableprodcuccion'] = ProductoProduccionTable(self.productoproduccion)
        else:
            context['existeproduccion'] = False
        return context
