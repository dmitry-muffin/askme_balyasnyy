import os
import django
from faker import Faker
from django.utils import timezone

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askme_balyasnyy.settings')
django.setup()

from django.contrib.auth.models import User
from app.models import Profile, Question, Tag, Answer

fake = Faker()

def create_users(num=5):
    print("Creating users...")
    users = []
    for _ in range(num):
        user = User.objects.create_user(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            password='testpass123'
        )
        profile = Profile.objects.create(user=user)
        users.append(profile)
        print(f"Created user: {user.username}")
    return users

def create_tags(num=15):
    print("\nCreating tags...")
    tags = []
    for _ in range(num):
        tag = Tag.objects.create(name=fake.unique.word().lower())
        tags.append(tag)
        print(f"Created tag: {tag.name}")
    return tags

def create_questions(users, tags, num=50):
    print("\nCreating questions...")
    questions = []
    for _ in range(num):
        question = Question.objects.create(
            owner=fake.random.choice(users),
            title=fake.sentence(),
            text=fake.text(),
            created_at=timezone.now()  # Добавляем текущую дату и время
        )
        question.tags.set(fake.random.sample(tags, k=3))
        questions.append(question)
        print(f"Created question: {question.title}")
    return questions

def create_answers(users, questions, num=200):
    print("\nCreating answers...")
    for _ in range(num):
        Answer.objects.create(
            owner=fake.random.choice(users),
            question=fake.random.choice(questions),
            text=fake.text(),
            created_at=timezone.now(),  # Добавляем текущую дату и время
            is_correct=fake.boolean(chance_of_getting_true=25)
        )
    print(f"Created {num} answers")

def main():
    try:
        users = create_users()
        tags = create_tags()
        questions = create_questions(users, tags)
        create_answers(users, questions)
        print("\nDatabase populated successfully!")
    except Exception as e:
        print(f"\nError: {e}\n")
        raise

if __name__ == '__main__':
    main()