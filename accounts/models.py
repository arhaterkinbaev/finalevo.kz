from django.db import models
from django.contrib.auth.models import AbstractUser

# Функция для хранения фото профиля пользователя
def user_directory_path(instance, filename):
    return f'profile_pictures/user_{instance.id}/{filename}'

# Кастомный пользователь с фото и био
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        default='default/profile.png'
    )

    def __str__(self):
        return self.username

# Функция для хранения фото продукта
def product_image_path(instance, filename):
    return f'product_images/{instance.name}/{filename}'

# Категории для удобства
CATEGORY_CHOICES = [
    ('laptop', 'Laptop'),
    ('smartphone', 'Smartphone'),
    ('accessory', 'Accessory'),
    ('tv', 'TV'),
]

# Модель продукта
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=product_image_path)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='laptop')

    def __str__(self):
        return self.name
