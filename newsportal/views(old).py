from django.shortcuts import render
from django.views.generic import ListView, DetailView  # импортируем класс получения деталей объекта
from .models import Post


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_post'] = Post.objects.all().count()
        return context


# создаём представление, в котором будут детали категории новости (о чем новость)
class NewDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали новости
    template_name = 'new.html'  # название шаблона будет new.html
    context_object_name = 'new'  # название объекта. в нём будет

