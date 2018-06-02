from django.db import models
from cliente.models import *
from producto.models import *
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null = True)
    factura = models.FileField(null=True, blank=True)
    no_de_factura = models.CharField(max_length=50,null=True, blank=True)
    fecha_creacion = models.DateField(default=timezone.now)
    limite_de_pago = models.DateField(default = timezone.now)
    a_cuenta = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    falta = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    iva = models.DecimalField(max_digits = 2, decimal_places = 0, default = 0)
    total = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    validar = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return 'V'+ '%06d' % int(self.id)

    def referencia(self):
        return 'V'+ '%06d' % int(self.id)

    def acciones(self):
        return format_html('<a class="btn btn-primary" href=/venta/{}/eliminar role="button">\
                                <em class="fa fa-times">&nbsp;</em></a>\
                            <a class="btn btn-primary" href=/venta/{}/update role="button">\
                                <em class="fa fa-pencil-square-o"></em></a>\
                            <a class="btn btn-primary" href=/venta/{}/reporte role="button">\
                                <em class="fa fa-file"></em></a>\
                            <a class="btn btn-primary" href=/venta/{}/pago role="button">\
                                <em class="fa fa-money"></em></a>',
                            self.pk,self.pk,self.pk,self.pk)

    def estado(self):
        if(self.validar == 0):
            return format_html('<span style="color: #FF5733;">No validado</span>',)
        if(self.validar == 1):
            return format_html('<span style="color: #27BC59;">Validado</span>',)

    def pagado(self):
        if(self.falta > 0):
            return format_html('<span style="color: #FF5733;">No pagado</span>',)
        else:
            return format_html('<span style="color: #27BC59;">Pagado</span>',)

    def save(self, *args, **kwargs):
        self.limite_de_pago = self.fecha_creacion + timedelta(self.cliente.credito)
        super(Venta, self).save(*args, **kwargs)

    def pago(self):
        if(self.falta > 0):
            return 'No pagado'
        else:
            return 'Pagado'



class ProductoVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null = True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits = 10, decimal_places = 3, default = 0.000)

    def save(self, *args, **kwargs):
        ajuste = Producto.objects.get(id=self.producto.id)
        venta = Venta.objects.get(id=self.venta.id)
        iva = (100 + self.venta.iva) / 100
        ajuste.stock -= self.cantidad
        venta.total += self.producto.precio_de_venta * iva * self.cantidad
        venta.falta = venta.total - venta.a_cuenta
        venta.save()
        ajuste.save()
        super(ProductoVenta, self).save(*args, **kwargs)

    def acciones(self):
        if not self.venta.validar:
            return format_html('<a class="btn btn-primary" href=/venta/producto/{}/eliminar role="button">X</a>',
                            self.pk)
        return

class PagoVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null = True)
    pago = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    fecha_de_pago = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        venta = Venta.objects.get(id=self.venta.id)
        venta.a_cuenta += self.pago
        venta.falta = venta.total - venta.a_cuenta
        venta.save()
        super(PagoVenta, self).save(*args, **kwargs)

    def acciones(self):
        return format_html('<a class="btn btn-primary" href=/venta/pago/{}/eliminar role="button">X</a>',
                            self.pk)


@receiver(pre_delete, sender=ProductoVenta)
def EliminarProductoVenta(sender, instance, **kwargs):
    venta = Venta.objects.get(id=instance.venta.id)
    ajuste = Producto.objects.get(id=instance.producto.id)
    iva = (100 + venta.iva)/100
    venta.total -= instance.producto.precio_de_venta * iva * instance.cantidad
    venta.falta = venta.total - venta.a_cuenta
    ajuste.stock += instance.cantidad
    ajuste.save()
    venta.save()

@receiver(pre_delete, sender=PagoVenta)
def EliminarPagoVenta(sender, instance, **kwargs):
    venta = Venta.objects.get(id=instance.venta.id)
    venta.a_cuenta -= instance.pago
    venta.falta = venta.total - venta.a_cuenta
    venta.save()
