from .models import Post
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment
from .forms import CommentForm

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        content = request.POST.get('contenido')
        if request.user.is_authenticated:
            Comment.objects.create(article=article, author=request.user, content=content)
            return redirect('articulos', article_id=contenido.id)

    return render(request, 'lista_contenidos.html', {'contenido': article})
