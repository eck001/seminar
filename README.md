# Seminar

0.0 -> Die Ausgabedaten des Tweetscraper von werden in der DataBase gespeichert


1-)Requirements herunterladen

-- In Konsole:

2-)python manage.py makemigrations

3-)python manage.py migrate

4-)scrapy crawl TweetScraper -a query="from: since: until:"   (from:Name des Unternehmens since:360 Tage vor Databreach until:29 Tage nach Databreach)

5-)python manage.py createdetails Unternehmensname Datum      (Datum = Datum des Breaches in 2021-01-30 Format)

6-)python manage.py runserver



**BEFEHLE:**

    -Delete all objects
    
    in Shell (python manage.py shell)
    from unternehmen.models import *
    Tweets.objects.all().delete()

    -filter
    from unternehmen.models import *
    q = unternehmen.objects.filter(unternehmensname = 'Yahoo',...)
    unternehmen.objects.filter(unternehmensname = 'Yahoo',...).delete() 

	
        

