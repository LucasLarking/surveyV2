from django.db import models

# Create your models here.


class Survey(models.Model):
    survey = models.CharField(max_length=200)

    def get_questions(self):
        return self.question_set.all()

    def number_of_questions(self):
        return self.question_set.all().count()

    def __str__(self):
        return self.survey


questionTypes = [
    ('radio', 'radio'),
    ('checkbox', 'checkbox'),
]


class Question(models.Model):
    question = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    showOtherField = models.BooleanField(default=False)

    question_type = models.CharField(
        choices=questionTypes,
        max_length=200,
        null=True,
        blank=True,
        default=questionTypes[0][0]
    )

    def get_options(self):
        return self.option_set.all()

    def number_of_options(self):
        return self.option_set.all().count()

    def __str__(self):
        return self.question


class Option(models.Model):
    option = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def get_votes(self):
        return self.vote_set.all().count()

    def __str__(self):
        return self.option


class OtherField(models.Model):

    otherField = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.otherField


class Vote(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    vote = models.BooleanField(default=True)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.vote)
