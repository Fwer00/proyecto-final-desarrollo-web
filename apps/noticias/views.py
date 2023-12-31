from django.shortcuts import render, HttpResponse, redirect
from .models import Noticia, Categoria, Comentario
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.views.generic.base import View
from .forms import ComentarioForm, NoticiaForm, CategoriaForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404



class Inicio(View):
    def get(self, request, *args, **kwargs):
        id_categoria = request.GET.get('id', None)
        ATOZID = request.GET.get('ATOZ')
        ZTOAID = request.GET.get('ZTOA')
        RTOAID = request.GET.get('RTOA')
        ATORID = request.GET.get('ATOR')
        print(ATOZID)
        if id_categoria:
            n = Noticia.objects.filter(categoria_noticia=id_categoria)
        elif ATOZID:
            n = Noticia.objects.order_by('titulo')
        elif ZTOAID:
            n = Noticia.objects.order_by('-titulo')
        elif RTOAID:
            n = Noticia.objects.order_by('-fecha')
        elif ATORID:
            n = Noticia.objects.order_by('fecha')
        else:
            n = Noticia.objects.all() 

        cate = Categoria.objects.all().order_by('nombre')
        contexto = {
            'noticias':n,
            'categorias': cate,
        }
        return render(request, 'noticias/inicio.html', contexto)


class Contenido_Noticias(View):
    def get(self, request, pk, *args, **kwargs):
        noticia = Noticia.objects.get(pk=pk)
        comentarios = Comentario.objects.filter(noticia=noticia).order_by('-fecha')

        contexto = {
            'noticia':noticia,
            'comentarios':comentarios,
        }
        return render(request, 'noticias/contenido.html', contexto)
    
    def noticia(self, request, pk, *args, **kwargs):
        noticia = Noticia.objects.get(pk=pk)

        comentarios = Comentario.objects.filter(noticia=noticia).order_by('-fecha')
        contexto = {
            'noticia':noticia,
            'comentarios':comentarios,
        }
        return render(request, 'noticias/contenido.html', contexto)
    

class Editar_ComentarioView(UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'noticias/edicion.html'

    def get_success_url(self):
        comentario = self.object
        url_noticia = comentario.noticia.get_absolute_url()
        return url_noticia


#porsiacaso
#def Eliminar_Comentario(request, id):
#   com = Comentario.objects.filter(id=id)
#   com.delete()
#   return redirect(reverse_lazy('noticias:inicio'))

#def Eliminar_Comentario(request, id):
#    comment = Comentario.objects.get(id=id)
#    comment.delete()
#    return redirect(reverse_lazy('noticias:inicio'))

def Eliminar_Comentario(request, id):
    comment = get_object_or_404(Comentario, id=id)
    noticia_id = comment.noticia.id  # Obtener el id de la noticia relacionada al comentario
    comment.delete()

    redirect_url = f'/noticias/{noticia_id}/'
    
    return redirect(redirect_url)

@login_required
def Comentar_Noticia(request):
    comentario = request.POST.get('comentario', None)
    user = request.user
    noti = request.POST.get('id_noticia', None)
    noticia = Noticia.objects.get(pk=noti)
    coment = Comentario.objects.create(
         usuario=user ,noticia=noticia, texto=comentario)
    return redirect(reverse_lazy('noticias:contenido', kwargs={"pk": noti}))

class Editar_NoticiaView(UpdateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'noticias/editar_noticia.html'

    def get_success_url(self):
        noticia = self.object
        url_noticia = noticia.get_absolute_url()
        return url_noticia
    
class Crear_NoticiaView(CreateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'noticias/crear_noticia.html'

    def get_success_url(self):
        return reverse_lazy('noticias:inicio')
    
def Eliminar_Noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    noticia.delete()
    
    return redirect('noticias:inicio')

class Crear_CategoriaView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'noticias/crear_categoria.html'

    def get_success_url(self):
        return reverse_lazy('noticias:inicio')

#BRRA BUSQUEDA
def busqueda(request):
    if request.method == "POST":
        busquedaa = request.POST['busquedaa']
        resultados = Noticia.objects.filter(titulo__contains=busquedaa)

        return render(request, 'busqueda.html', {'busquedaa':busquedaa,
                                                 'resultados': resultados})
    else:
        return render(request, 'busqueda.html', {})
    


