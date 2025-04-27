from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('chat/', views.chat_page, name='chat_page'),
    path('chatbot-reply/', views.chatbot_reply, name='chatbot_reply'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('catalog/', views.catalog, name='catalog'),
    path('logout/', views.logout_view, name='logout'),
path('clear-history/', views.clear_chat_history, name='clear_chat_history'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
