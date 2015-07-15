from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def main(request):
    return render(request, 'main.html')




### este es el mockup de las rutas.

def route(request):
    #origin = self.request.get('origin')
    #destination = self.request.get('destination')
    #self.render('route.html', origin=origin, destination=destination)
    #return render(request, 'routes.html')
    return render(request, 'route.html')
