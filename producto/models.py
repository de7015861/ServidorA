from django.db import models
from django.utils.html import format_html
from django.utils import timezone

# Create your models here.
class Producto(models.Model):
    TIPO_CHOISE = ( ('Consumible', 'Consumible'),
                    ('Servicio', 'Servicio'),
                    ('Almacenable', 'Almacenable'),
                  )

    producto = models.CharField(max_length=50)
    detalles = models.CharField(max_length=50)
    codigo_de_barras = models.CharField(max_length=50, unique = True)
    tipo_del_producto = models.CharField(max_length=50,choices = TIPO_CHOISE)
    stock = models.DecimalField(max_digits = 10, decimal_places = 3, default = 0.000)
    stock_minimo = models.DecimalField(max_digits = 10, decimal_places = 3, default = 0.000)
    unidades = models.CharField(max_length=50)
    costo = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    precio_de_venta = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    fecha_creacion = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['producto']

    def __str__(self):
        return  self.producto

    def acciones(self):
        return format_html('<a class="btn btn-primary" href=/producto/{}/eliminar role="button">\
                                <em class="fa fa-times">&nbsp;</em></a>\
                            <a class="btn btn-primary" href=/producto/{}/update role="button">\
                                <em class="fa fa-pencil-square-o"></em></a>',
                            self.pk,self.pk,self.pk)
