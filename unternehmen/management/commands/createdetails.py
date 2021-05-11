from django.core.management.base import BaseCommand
from unternehmen.models import *
import datetime


class Command(BaseCommand):
    def add_arguments(self, parser):                         # arguments des Commands festlegen
        parser.add_argument('name', type=str)
        parser.add_argument('datum', type=str)

    def handle(self, *args, **options):
        name = options["name"]
        datum = options["datum"]                              # eingabewerte in variablen speichern
        date_time_obj = datetime.datetime.strptime(datum, '%Y-%m-%d').date() #datum string als date_time_obj für operationen mit timedelta

        tdelta1 = datetime.timedelta(days=9)            # timedeltas für verschiedene Zeiträume festlegen
        tdelta2 = datetime.timedelta(days=19)
        tdelta3 = datetime.timedelta(days=29)

        tdeltabefore1 = datetime.timedelta(days=360)
        tdeltabefore2 = datetime.timedelta(days=1)

        # tweets des gesamten Zeitraums auf die Splits und before aufteilen, mittels timedelta und datum__range
        tweetsfirstsplit = Tweets.objects.filter(unternehmensname=name,
                                                 datum__range=[datum, str(date_time_obj + tdelta1)])
        tweetssecondsplit = Tweets.objects.filter(unternehmensname=name,
                                                  datum__range=[datum, str(date_time_obj + tdelta2)])
        tweetsthirdsplit = Tweets.objects.filter(unternehmensname=name,
                                                 datum__range=[datum, str(date_time_obj + tdelta3)])
        tweetsbefore = Tweets.objects.filter(unternehmensname=name, datum__range=[str(date_time_obj - tdeltabefore1),
                                                                                  str(date_time_obj - tdeltabefore2)])


        tweetsumme = 0          # für jeden split tweetsumme berechnen, und abschließen average_words für gesamten 30 Tage Zeitraum

        for i in tweetsfirstsplit:
            tweetsumme += 1
        tweets_after_10_days = tweetsumme

        tweetsumme = 0

        for i in tweetssecondsplit:
            tweetsumme += 1
        tweets_after_20_days = tweetsumme

        tweetsumme = 0
        woertersumme = 0

        for i in tweetsthirdsplit:
            tweetsumme += 1
            woertersumme += i.woerter
        tweets_after_30_days = tweetsumme
        average_words = woertersumme / tweetsumme

        details.objects.create(                 # details objekt für nach den dem Databreach erstellen
            unternehmensname=tweetsthirdsplit.first().unternehmensname,
            woerteranzahl=woertersumme,
            tweetsanzahl=tweetsumme,
            vorodernach="nach",
            average_words=average_words,
            tweets_per_30_days=tweetsumme,
            tweets_after_10_days=tweets_after_10_days,
            tweets_after_20_days=tweets_after_20_days,
            tweets_after_30_days=tweets_after_30_days,
        )

        woertersumme = 0                    # Daten für Tweets vor dem Databrach ermitteln

        tweetsumme = 0

        for i in tweetsbefore:
            woertersumme += i.woerter

            tweetsumme += 1

        average_words = woertersumme / tweetsumme
        tweets_per_30_days_before = tweetsumme / 360 * 30

        details.objects.create(             # details objekt für vor den dem Databreach erstellen
            unternehmensname=tweetsbefore.first().unternehmensname,
            woerteranzahl=woertersumme,

            tweets_per_30_days=tweets_per_30_days_before,
            average_words=average_words,
            tweetsanzahl=tweetsumme,
            vorodernach="vor"
        )
