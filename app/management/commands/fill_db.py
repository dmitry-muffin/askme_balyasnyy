import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from app.models import Profile, Tag, Question, Answer, QuestionVote, AnswerVote

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными. Использование: python manage.py fill_db [ratio]'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения сущностей')

    def handle(self, *args, **options):
        ratio = options['ratio']
        self.stdout.write(f"Запуск заполнения БД с ratio = {ratio}")

        now = timezone.now()

        # Создание тегов
        self.stdout.write("Создание тегов...")
        tags = []
        for i in range(ratio):
            tag = Tag(name=f"tag_{i}")
            tags.append(tag)
        Tag.objects.bulk_create(tags)
        tags = list(Tag.objects.all())  # перечитаем теги из БД

        # Создание пользователей и профилей
        self.stdout.write("Создание пользователей и профилей...")
        profiles = []
        for i in range(ratio):
            username = f"user_{i}"
            email = f"user_{i}@example.com"
            user = User.objects.create_user(username=username, email=email, password="password")
            profile = Profile(user=user)
            profiles.append(profile)
        Profile.objects.bulk_create(profiles)
        profiles = list(Profile.objects.all())

        # Создание вопросов
        self.stdout.write("Создание вопросов...")
        num_questions = ratio * 10
        questions = []
        for i in range(num_questions):
            owner = random.choice(profiles)
            question = Question(
                owner=owner,
                title=f"Вопрос {i}",
                text=f"Текст вопроса {i}. Здесь может быть подробное описание проблемы.",
                created_at=now - timedelta(days=random.randint(0, 365))
            )
            questions.append(question)
        Question.objects.bulk_create(questions)
        questions = list(Question.objects.all())

        # Назначение тегов для вопросов
        self.stdout.write("Привязка тегов к вопросам...")
        for question in questions:
            # Выбираем от 1 до 3 случайных тегов для каждого вопроса
            question_tags = random.sample(tags, k=random.randint(1, min(3, len(tags))))
            question.tags.add(*question_tags)

        # Создание ответов
        self.stdout.write("Создание ответов...")
        num_answers = ratio * 100
        answers = []
        for i in range(num_answers):
            owner = random.choice(profiles)
            question = random.choice(questions)
            answer = Answer(
                owner=owner,
                question=question,
                text=f"Ответ {i}. Это текст ответа на вопрос.",
                created_at=now - timedelta(days=random.randint(0, 365))
            )
            answers.append(answer)
        Answer.objects.bulk_create(answers)
        answers = list(Answer.objects.all())

        # Создание голосований (вопросов и ответов)
        self.stdout.write("Создание голосований...")
        num_votes = ratio * 200
        question_votes = []
        answer_votes = []
        # Используем множества для отслеживания уникальных пар (owner_id, question_id) и (owner_id, answer_id)
        question_vote_keys = set()
        answer_vote_keys = set()

        for i in range(num_votes):
            owner = random.choice(profiles)
            is_positive = random.choice([True, False])
            created = now - timedelta(days=random.randint(0, 365))
            # Решаем голосовать за вопрос или за ответ
            if random.choice([True, False]) and questions:
                question = random.choice(questions)
                key = (owner.id, question.id)
                if key in question_vote_keys:
                    continue  # Пропускаем, если голос уже есть
                question_vote_keys.add(key)
                vote = QuestionVote(
                    owner=owner,
                    question=question,
                    is_positive=is_positive,
                    created_at=created
                )
                question_votes.append(vote)
            elif answers:
                answer = random.choice(answers)
                key = (owner.id, answer.id)
                if key in answer_vote_keys:
                    continue  # Пропускаем, если голос уже есть
                answer_vote_keys.add(key)
                vote = AnswerVote(
                    owner=owner,
                    answer=answer,
                    is_positive=is_positive,
                    created_at=created
                )
                answer_votes.append(vote)

        # Создаём голосования пакетно
        if question_votes:
            QuestionVote.objects.bulk_create(question_votes)
        if answer_votes:
            AnswerVote.objects.bulk_create(answer_votes)

        self.stdout.write(self.style.SUCCESS("Заполнение базы данных завершено!"))
