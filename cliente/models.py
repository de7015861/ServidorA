from django.db import models
from django.utils.html import format_html

# Create your models here.
class Cliente(models.Model):
    CREDITO_CHOISE = ( (0, 'No'),
                       (15, '15d'),
                       (30, '30d'),
                     )
    contacto = models.CharField(max_length=50)
    direccion_entrega = models.CharField(max_length=50)
    razon_social = models.CharField(max_length=50)
    rfc = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=5)
    ciudad = models.CharField(max_length=50)
    credito = models.IntegerField(default = 0, choices = CREDITO_CHOISE)
    correo = models.EmailField()
    telefono = models.CharField(max_length=50)

    class Meta:
        ordering = ['razon_social']

    def __str__(self):
        return self.razon_social

    def acciones(self):
        return format_html('<a class="btn btn-primary" href=/cliente/{}/eliminar role="button">\
                                <em class="fa fa-times">&nbsp;</em></a>\
                            <a class="btn btn-primary" href=/cliente/{}/update role="button">\
                                <em class="fa fa-pencil-square-o"></em></a>',
                            self.pk,self.pk,self.pk)
