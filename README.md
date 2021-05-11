# Seminar

1-) Bei der Entwicklung des Projekts wurde das vorgeschribene Program "TweetScraper" verwendet.

    https://github.com/jonbakerfish/TweetScraper

2-)Damit das Programm einwandfrei funktioniert, müssen die Packages(requirements.txt) heruntergeladen werden.

**Im folgenden Schritten wurde als Beispiel das Unternehmen "Mastercard" verwendet.(Datum des Databreaches : 19.08.2019)**

3-)Für der Sammlung der Daten muss der folgende Befehl eingegeben werden

    scrapy crawl TweetScraper -a query="from:Mastercard since:2018-08-24 until:2019-09-17"
    (from:Name des Unternehmens since:360 Tage vor Databreach until:29 Tage nach Databreach)
    Für die Erstellung des Objekts muss der Unternehmensname nochmal manuell eingegeben werden
    Um nur von dem Unternehmen geposteten Tweets zu sammeln, muss der Schlüssel-ID manuell eingegeben werden
    Für die Bestimmung der Schlüssel-ID kann die Webseite "https://tweeterid.com)" verwendet werden

Nach diesem Befehl werden die Informationen in die Klasse "Tweets" gepeichert.Für jeder Tweet wird ein neues Objekt erstellt.

4-)Um die Informationen zusammenzufassen und die Zusammenfassung in die Klasse "Details" zu speichern muss der folgender Befehl eingegeben werden

    python manage.py createdetails Mastercard 2019-08-19
    (Datum des Breaches in 2019-08-19 Format)
Nach diesem Befelh werden die Informationen zusammengefasst in die Klasse "Details" gespeichert.
Insgesamt werden 2 Objekten erstellt(Vor und Nach dem Data Breach)
    




#extra

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

	
        

