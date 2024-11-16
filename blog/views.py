from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment
from django.shortcuts import redirect
from django.urls import reverse

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        """Adiciona os comentários ao contexto da página de detalhe do post"""
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-date_posted')  # Comentários ordenados
        return context

    def post(self, request, *args, **kwargs):
        """Lida com o envio de novos comentários"""
        self.object = self.get_object()  # Obtém o objeto do post
        content = request.POST.get('content')  # Obtém o conteúdo do comentário do formulário
        author = request.user if request.user.is_authenticated else None  # Define o autor (ou None)

        if content:  # Verifica se o comentário não está vazio
            Comment.objects.create(
                post=self.object,
                author=author,
                content=content,
            )
        return redirect('post-detail', pk=self.object.pk)
    
    
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        """Redireciona para a página do post associado após exclusão do comentário"""
        post_id = self.object.post.id  # Obtém o ID do post relacionado
        return reverse('post-detail', kwargs={'pk': post_id})