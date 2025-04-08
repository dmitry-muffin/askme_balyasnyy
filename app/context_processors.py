from django.contrib.auth.models import User
from django.core.cache import cache

from app.models import Tag, Profile

def popular_tags(request):
    tags = cache.get('popular_tags')
    if tags is None:
        tags = Tag.objects.get_popular()
        cache.set('popular_tags', tags, 300)  # 5 минут
    return {'popular_tags': tags}

def best_users(request):
    # Берем 5 лучших пользователей
    users = cache.get('best_users')
    if users is  None:
        users = Profile.objects.get_best()
        cache.set('best_users', users, 300)
    return {'best_users': users}