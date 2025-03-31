import os
import django
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.contrib.auth.models import User
from app.models import Profile, Question, Tag, Answer

fake = Faker()


def create_users(num=5):
    users = []
    for _ in range(num):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password='testpass123'
        )
        profile = Profile.objects.create(
            user=user,
            avatar='uploads/default.png'
        )
        users.append(profile)
    return users


def create_tags(num=10):
    tags = []
    for _ in range(num):
        tag = Tag.objects.create(name=fake.word())
        tags.append(tag)
    return tags


def create_questions(users, tags, num=20):
    for _ in range(num):
        question = Question.objects.create(
            owner=fake.random.choice(users),
            title=fake.sentence(),
            text=fake.text(),
            created_at=fake.date_time_this_year()
        )
        question.tags.set(fake.random.sample(tags, k=3))


def create_answers(users, questions, num=50):
    for _ in range(num):
        Answer.objects.create(
            owner=fake.random.choice(users),
            question=fake.random.choice(questions),
            text=fake.text(),
            created_at=fake.date_time_this_year()
        )


def main():
    users = create_users()
    tags = create_tags()
    create_questions(users, tags)
    questions = Question.objects.all()
    create_answers(users, questions)
    print("Test data created successfully!")


if __name__ == '__main__':
    main()