from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Endereco
from .forms import EnderecoForm
from django.shortcuts import redirect
import pycep_correios
import googlemaps

# Create your views here.

def mapa(request, cid, uf, br):
    gmaps = googlemaps.Client(key='AIzaSyDNzTsrViW4U2C7UxVK61PmE6Xmvp3wK74')
    # Geocoding an address
    geocode_result = gmaps.geocode(cid + ', '+ uf+ ', '+ br)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]

    return render(request, 'myapp/mapa.html', {'latitude': str(lat), 'longitude': str(lon) })
    #return render(request, 'myapp/mapa.html', {'latitude': -22.912869, 'longitude': -43.228963 })


def endereco_list(request):
    enderecos = Endereco.objects.all()
    return render(request, 'myapp/endereco_list.html', {'enderecos': enderecos})

def endereco_detail(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    return render(request, 'myapp/endereco_detail.html', {'endereco': endereco})
  
def busca_cep(request):
    if request.method == "POST":
        print('passei aqui')
        cep = request.POST['cep']
        ender = pycep_correios.consultar_cep(cep)
        
        data = {
            'estado': ender['uf'],
            'cidade': ender['cidade'],
            'logradouro': ender['end'],
            'bairro': ender['bairro'],
            'cep': ender['cep'],
        }
        form = EnderecoForm(data)
        
        #form = EnderecoForm()
        #form["estado"] = 
        return render(request, 'myapp/endereco_edit.html', {'form': form})
    else:
        return render(request, 'myapp/buscar_cep.html', {})
  
def endereco_new(request):
    print('passei aqui')
    if request.method == "POST":
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.save()
            return redirect('endereco_detail', pk=endereco.pk)
    else:
        form = EnderecoForm()
    return render(request, 'myapp/endereco_edit.html', {'form': form})
    
def endereco_edit(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    if request.method == "POST":
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.save()
            return redirect('endereco_detail', pk=endereco.pk)
    else:
        form = EnderecoForm(instance=endereco)
    return render(request, 'myapp/endereco_edit.html', {'form': form})
    
def endereco_remove(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    endereco.delete()
    return redirect('endereco_list')    
    
