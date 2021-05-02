from django.db import models
from datetime import datetime


# Create your models here.

class Tweets(models.Model):                 # Model Tweets mit allen  relevanten Infos eines Tweets
    unternehmensname = models.CharField(max_length=100, default='--')
    userId = models.CharField(max_length=100, default='--')
    datum = models.DateField(max_length=20, default='--')
    woerter = models.IntegerField(default=0)
    schluesselId = models.CharField(max_length=100, default='', editable=False)

    def __str__(self):                  # string funktion für Tweets
        return  "Unternehmensname = " + self.unternehmensname + "\t|" \
                "datum = " + str(self.datum) + "\t|" \
                "Wörteranzahl = " + str(self.woerter)

    class Meta:
        verbose_name = "Tweet"
        verbose_name_plural = "Tweets"


class details(models.Model):            # Model details für Zusammenfassung der KeyFacts
    unternehmensname = models.CharField(max_length=100, default='--')
    vorodernach = models.CharField(max_length=20, default='--')
    tweetsanzahl = models.IntegerField(default=0)
    woerteranzahl = models.IntegerField(default=0)
    average_words = models.FloatField(default = 0)
    tweets_per_30_days = models.FloatField(default=0)
    tweets_after_10_days = models.IntegerField(null=True)         #nur relevant für nach Data Breach
    tweets_after_20_days = models.IntegerField(null=True)         #
    tweets_after_30_days = models.IntegerField(null=True)         #IntegerField



    def __str__(self):
        return  self.unternehmensname + "\t" + self.vorodernach + " dem Data Breach" \
                "\tGesamte Tweetsanzahl = " + str(self.tweetsanzahl) + \
                "\tGesamte Wörteranzahl = " + str(self.woerteranzahl)


    class Meta:
        verbose_name = "Details"
        verbose_name_plural = "Details"
