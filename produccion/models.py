from django.db import models
from django.utils import timezone
from producto.models import *
from django.dispatch import receiver
from django.db.models.signals import pre_delete

# Create your models here.
class Produccion(models.Model):
    descripcion = models.CharField(max_length=50, null=True)
    validar = models.BooleanField(default=False)
    fecha_creacion = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return 'P'+ '%06d' % int(self.id)

    def referencia(self):
        return 'P'+ '%06d' % int(self.id)

    def acciones(self):
        return format_html('<a class="btn btn-primary" href=/produccion/{}/eliminar role="button">\
                                <em class="fa fa-times">&nbsp;</em></a>\
                            <a class="btn btn-primary" href=/produccion/{}/update role="button">\
                                <em class="fa fa-pencil-square-o"></em></a>\
                            <a class="btn btn-primary" href=/produccion/{}/reporte role="button">\
                                <em class="fa fa-file"></em></a>',
                            self.pk,self.pk,self.pk)

    def estado(self):
        if(self.validar == 0):
            return format_html('<span style="color: #FF5733;">No validado</span>',)
        if(self.validar == 1):
            return format_html('<span style="color: #27BC59;">Validado</span>',)

class ProductoProduccion(models.Model):
    produccion = models.ForeignKey(Produccion, on_delete=models.CASCADE, null = True)
    producto_para_producir = models.ForeignKey(Producto, on_delete=models.CASCADE, null = False,related_name="%(class)s_producir")
    cantidad_para_producir = models.DecimalField(max_digits = 10, decimal_places = 3, default = 0.000)
    producto_producido = models.ForeignKey(Producto, on_delete=models.CASCADE, null = False,related_name="%(class)s_producido")
    cantidad_producido = models.DecimalField(max_digits = 10, decimal_places = 3, default = 0.000)

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        ajuste = Producto.objects.get(id=self.producto_para_producir.id)
        ajuste.stock -= self.cantidad_para_producir
        ajuste.save()
        ajuste = Producto.objects.get(id=self.producto_producido.id)
        ajuste.stock += self.cantidad_producido
        ajuste.save()
        super(ProductoProduccion, self).save(*args, **kwargs)

    def acciones(self):
        if not self.produccion.validar:
            return format_html('<a class="btn btn-primary" href=/produccion/producto/{}/eliminar role="button">X</a>',
                            self.pk)
        return


@receiver(pre_delete, sender=ProductoProduccion)
def Eliminar_producir(sender, instance, **kwargs):
    ajuste = Producto.objects.get(id=instance.producto_para_producir.id)
    ajuste.stock += instance.cantidad_para_producir
    ajuste.save()
    ajuste = Producto.objects.get(id=instance.producto_producido.id)
    ajuste.stock -= instance.cantidad_producido
    ajuste.save()
