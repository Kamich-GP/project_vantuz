from django.shortcuts import render, redirect
from .models import Product, Category
from .forms import SearchForm, RegisterForm
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import logout, login


# Create your views here.
# Главная страница
def home_page(request):
    # Достаем данные из БД
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    # Достаем форму поиска
    search = SearchForm()
    # Передаем данные на фронт
    context = {'products': all_products, 'categories': all_categories, 'form': search}
    # Прогружаем html файл
    return render(request, 'home.html', context)


# Страница с товарами по категории
def category_page(request, pk):
    # Достаем выбранную категорию
    category = Category.objects.get(id=pk)
    # Фильтруем продукты по выбранной категории
    exact_products = Product.objects.filter(pr_category=category)
    # Передаем данные на фронт
    context = {'products': exact_products}
    # Прогружаем html файл
    return render(request, 'category.html', context)


# Страница с выбранным товаром
def product_page(request, pk):
    # Достаем выбранный товар
    product = Product.objects.filter(id=pk)
    # Передаем данные на фронт
    context = {'product': product}
    # Прогружаем html файл
    return render(request, 'product.html', context)


def search_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')

        if get_product:
            product = Product.objects.get(pr_name__icontains=get_product)
            return redirect(f'/product/{product.id}')
        else:
            return redirect('/')


# Регистрация
class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {'form': RegisterForm}
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterForm(request.POST)

        # Если данные корректны
        if form.is_valid():
            username = form.clean_username()
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username=username, password=password2,
                                            email=email)
            user.save()
            login(request, user)
            return redirect('/')
        # Если данные не совпали
        context = {'form': RegisterForm}
        return render(request, self.template_name, context)


def logout_view(request):
    logout(request)
    return redirect('/')
