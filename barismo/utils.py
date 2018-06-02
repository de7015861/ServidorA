
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.views import View
from producto.models import Producto


class ProductoPDFView(View):
    objeto = Producto

    def get(self, request, pk):
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        p = canvas.Canvas(buffer, 'letter')
        p.drawString(100, 100, 'Hello world.')
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
