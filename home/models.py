from django.db import models


class Prono(models.Model):
    match_date = models.CharField(max_length=40)
    time = models.CharField(max_length=40)
    teams = models.CharField(max_length=400, primary_key=True)
    chance = models.CharField(max_length=40)
    odd1 = models.CharField(max_length=40)
    oddX = models.CharField(max_length=40)
    odd2 = models.CharField(max_length=40)
    win_odd = models.CharField(max_length=20)
    match_result = models.CharField(max_length=40)
    result_overall = models.CharField(max_length=20)

    def __str__(self):
        return self.match_date

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


