from django.shortcuts import render, redirect
from .models import Product, Category, Cart
from .forms import SearchForm, RegisterForm
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import logout, login
import telebot

# Создаем объект бота
bot = telebot.TeleBot('7487631864:AAEdSHEE6XWsK6EeroHYTt_qsyyfjtFJAbs')
admin_id = 6775701667


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


# Добавление товара в корзину
def to_cart(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        if product.pr_count >= int(request.POST.get('pr_quantity')):
            Cart.objects.create(user_id=request.user.id,
                                user_product=product,
                                user_product_quantity=int(request.POST.get('pr_quantity'))).save()

        return redirect('/')


# Отображение корзины
def cart(request):
    user_cart = Cart.objects.filter(user_id=request.user.id)
    pr_id = [i.user_product.id for i in user_cart]
    pr_prices = [e.user_product.pr_price for e in user_cart]
    user_pr_amount = [c.user_product_quantity for c in user_cart]
    pr_amount = [a.user_product.pr_count for a in user_cart]
    total = 0
    text = (f'Новый заказ!\n\n'
            f'Клиент: {User.objects.get(id=request.user.id).username}\n')

    for p in range(len(pr_prices)):
        total += user_pr_amount[p] * pr_prices[p]

    if request.method == 'POST':
        for i in user_cart:
            text += (f'Товар: {i.user_product}\n'
                     f'Количество: {i.user_product_quantity}')
        text += f'Итог: ${round(total, 2)}'
        bot.send_message(admin_id, text)
        for u in range(len(pr_prices)):
            product = Product.objects.get(id=pr_id[u])
            product.pr_count = pr_amount[u] - user_pr_amount[u]
            product.save(update_fields=['pr_count'])
        user_cart.delete()
        return redirect('/')
    # Отправляем данные на фронт
    context = {'cart': user_cart, 'total': round(total, 2)}
    return render(request, 'cart.html', context)


def del_from_cart(request, pk):
    product_to_delete = Product.objects.get(id=pk)
    Cart.objects.filter(user_product=product_to_delete, user_id=request.user.id).delete()

    return redirect('/')
