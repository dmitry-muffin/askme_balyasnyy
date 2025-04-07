from app.models import Tag, Profile

def popular_tags(request):
    # Берем 10 самых популярных тегов
    tags = Tag.objects.get_popular()
    return {'popular_tags': tags}

def best_users(request):
    # Берем 5 лучших пользователей
    users = Profile.objects.get_best()
    return {'best_users': users}