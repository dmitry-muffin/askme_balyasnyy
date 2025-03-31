from django.db import models

class QuestionManager(models.Manager):
    def get_hot(self):
        return (self
                .all()
                .annotate(votes_num=models.Count('votes'))
                .order_by('-votes_num'))

    def get_new(self):
        return self.all().order_by('-created_at')

    def with_tags(self, tag_names):
        return self.filter(tags__name__in=tag_names).distinct()


    def votes_count(self) -> int:
        related_votes = self.question_likes.all()
        positive = related_votes.filter(is_positive=True).count()
        total = related_votes.count()
        return -total + positive * 2

    def answers_count(self) -> int:
        return self.answers.all().count()

class TagManager(models.Manager):
    def get_popular(self):
        return (self
                .all()
                .annotate(questions_num=models.Count('questions'))
                .order_by('-questions_num'))


class ProfileManager(models.Manager):
    def get_best(self):
        return (self
                .all()
                .annotate(activity=models.Count('questions')+models.Count('answers'))
                .order_by('-activity'))

    def answers_count(self) -> int:
        return self.answers.all().count()
