from django.shortcuts import render
from .models import Product, Category


# Create your views here.
# Главная страница
def home_page(request):
    # Достаем данные из БД
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    # Передаем данные на фронт
    context = {'products': all_products, 'categories': all_categories}
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
