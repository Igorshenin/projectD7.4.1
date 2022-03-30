from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView # импортируем уже знакомый generic
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод


from .models import Post, Category
from .filters import PostFilter  # импортируем недавно написанный фильтр
from .forms import PostForm


# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'news'
    ordering = ['-created']
    paginate_by = 10  # поставим постраничный вывод в один элемент

    def get_context_data(self,
                         **kwargs):  # забираем отфильтрованные объекты переопределяя метод
                                     # get_context_data у наследуемого класса (привет, полиморфизм,
                                     # мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                          queryset=self.get_queryset())  # вписываем наш фильтр
                                                                         # в контекст
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)

class NewDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали новости
    template_name = 'new.html'  # название шаблона будет new.html
    queryset = Post.objects.all()

class PostCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = PostForm


# дженерик для редактирования объекта
class PostUpdateView(UpdateView):
    template_name = 'news_update.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
