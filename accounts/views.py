from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .forms import RegisterForm, ProductForm
from .models import Product, CustomUser
from g4f.client import Client
import json
import os


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Регистрация прошла успешно. Добро пожаловать, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка в регистрации. Проверьте данные.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('home')


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def catalog(request):
    return render(request, 'catalog.html')


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def admin_home(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user
            product.save()
            messages.success(request, 'Товар успешно добавлен.')
            return redirect('admin_home')
    else:
        form = ProductForm()
    return render(request, 'admin_home.html', {'form': form})


@login_required
def chat_page(request):
    username = request.user.username
    history_path = os.path.join(settings.MEDIA_ROOT, 'chat', f'{username}_history.json')
    try:
        with open(history_path, 'r', encoding='utf-8') as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []
    return render(request, 'chat.html', {'history': history})


@csrf_exempt
def chatbot_reply(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        try:
            client = Client()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_message}],
                web_search=False
            )
            bot_response = response.choices[0].message.content
        except Exception as e:
            print("Ошибка GPT:", e)
            bot_response = "Извините, произошла ошибка при получении ответа от ИИ."

        username = request.user.username if request.user.is_authenticated else 'anonymous'
        history_path = os.path.join(settings.MEDIA_ROOT, 'chat', f'{username}_history.json')

        try:
            with open(history_path, 'r', encoding='utf-8') as file:
                history = json.load(file)
        except FileNotFoundError:
            history = []

        history.append({"user": user_message, "bot": bot_response})

        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        with open(history_path, 'w', encoding='utf-8') as file:
            json.dump(history, file, ensure_ascii=False, indent=4)

        return JsonResponse({'response': bot_response})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def clear_chat_history(request):
    username = request.user.username
    history_path = os.path.join(settings.MEDIA_ROOT, 'chat', f'{username}_history.json')
    if os.path.exists(history_path):
        os.remove(history_path)
        messages.success(request, 'История чата успешно очищена.')
    else:
        messages.info(request, 'История чата уже пуста.')
    return redirect('chat_page')
