from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from producto.models import Producto
from django.dispatch import receiver
from django.db.models.signals import pre_delete

# Create your models here.
class Salida(models.Model):
    descripcion = models.CharField(max_length=50)
    validar = models.BooleanField(default=False)
    fecha_creacion = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-fecha_creacion']

    def referencia(self):
        return 'S'+ '%06d' % int(self.id)

    def __str__(self):
        return 'S'+ '%06d' % int(self.id)

    def acciones(self):
        return format_html('<a class="btn btn-primary" href=/salida/{}/eliminar role="button">\
                                <em class="fa fa-times">&nbsp;</em></a>\
                            <a class="btn btn-primary" href=/salida/{}/update role="button">\
                                <em class="fa fa-pencil-square-o"></em></a>\
                            <a class="btn btn-primary" href=/salida/{}/reporte role="button">\
                                <em class="fa fa-file"></em></a>',
                            self.pk,self.pk,self.pk)

    def estado(self):
        if(self.validar == 0):
            return format_html('<span style="color: #FF5733;">No validado</span>',)
        if(self.validar == 1):
            return format_html('<span style="color: #27BC59;">Validado</span>',)


class ProductoSalida(models.Model):
    salida = models.ForeignKey(Salida, null = True, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, null = True, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits = 10, decimal_places = 3, default = 0.000)

    class Meta:
        ordering = ['-id']

    def acciones(self):
        if not self.salida.validar:
            return format_html('<a class="btn btn-primary" href=/salida/producto/{}/eliminar role="button">X</a>',
                            self.pk)
        return

    def save(self, *args, **kwargs):
        producto= Producto.objects.get(id=self.producto.id)
        producto.stock -= self.cantidad
        producto.save()
        super().save(*args, **kwargs)


@receiver(pre_delete, sender=ProductoSalida)
def Eliminar_producto(sender, instance, **kwargs):
    ajuste = Producto.objects.get(id=instance.producto.id)
    ajuste.stock += instance.cantidad
    ajuste.save()
