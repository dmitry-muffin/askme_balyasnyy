import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from typing import Optional


class QuestionManager(models.Manager):
    def get_hot(self):
        return self.annotate(votes_diff=models.Count('question_votes')).order_by('-votes_diff')

    def get_new(self):
        return self.order_by('-created_at')

    def with_tag(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-created_at', '-id')

    def for_user(self, user):
        return self.filter(owner__user=user)


class TagManager(models.Manager):
    def get_popular(self, count=10):
        return (self.annotate(questions_count=models.Count('questions'))
                   .order_by('-questions_count')[:count])


class ProfileManager(models.Manager):
    def get_best(self, count=5):
        return (self.annotate(activity=models.Count('questions') + models.Count('answers'))
                   .order_by('-activity')[:count])


class Profile(models.Model):
    objects = ProfileManager()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="uploads", default="/static/img/img.jpg")

    @property
    def answers_count(self) -> int:
        return self.answers.all().count()

    def get_avatar_url(self):
        return self.avatar.url if self.avatar else '/static/img/img.jpg'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})


class Tag(models.Model):
    objects = TagManager()

    name = models.CharField(max_length=20, unique=True)


class Question(models.Model):
    objects = QuestionManager()

    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="questions")
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="questions")
    created_at = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.pk})

    @property
    def short_text(self):
        return self.text[:150] + '...' if len(self.text) > 150 else self.text

    @property
    def votes_count(self) -> int:
        related_votes = self.question_votes.all()
        positive = related_votes.filter(is_positive=True).count()
        total = related_votes.count()
        return -total + positive * 2

    @property
    def answers_count(self) -> int:
        return self.answers.all().count()


class Answer(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    is_correct = models.BooleanField(default=False)
    text = models.TextField()
    created_at = models.DateTimeField()

    def accept_answer(self):
        self.question.answers.update(is_correct=False)
        self.is_correct = True
        self.save()

    @property
    def votes_count(self):
        return self.answer_votes.all().count()


class AnswerVote(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="answer_votes")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="answer_votes")
    is_positive = models.BooleanField(help_text="Отмечает, положительный или отрицательный голос")
    created_at = models.DateTimeField()

    class Meta:
        unique_together = ('owner', 'answer')



class QuestionVote(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="question_votes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_votes")
    is_positive = models.BooleanField(help_text="Отмечает, положительный или отрицательный голос")
    created_at = models.DateTimeField()

    class Meta:
        unique_together = ('owner', 'question')
