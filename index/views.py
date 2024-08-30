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
