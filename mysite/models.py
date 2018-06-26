from django.db import models


class Prono(models.Model):
    date = models.CharField(max_length=40)
    time = models.CharField(max_length=40)
    teams = models.CharField(max_length=400)
    prob1 = models.CharField(max_length=40)
    probX = models.CharField(max_length=40)
    prob2 = models.CharField(max_length=40)
    chance = models.CharField(max_length=40)
    odd1 = models.CharField(max_length=40)
    oddX = models.CharField(max_length=40)
    odd2 = models.CharField(max_length=40)
    match_result = models.CharField(max_length=40)
    result_home = models.CharField(max_length=10)
    result_away = models.CharField(max_length=10)
    result_overall = models.CharField(max_length=20)

    def __str__(self):
        return self.date

    def __str__(self):
        return self.time

    def __str__(self):
        return self.teams

    def __str__(self):
        return self.prob1

    def __str__(self):
        return self.probX

    def __str__(self):
        return self.prob2

    def __str__(self):
        return self.chance

    def __str__(self):
        return self.odd1

    def __str__(self):
        return self.oddX

    def __str__(self):
        return self.odd2

    def __str__(self):
        return self.result_away

    def __str__(self):
        return self.result_home

