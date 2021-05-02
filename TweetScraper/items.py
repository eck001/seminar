from scrapy import Item, Field
from unternehmen.models import Tweets,details
from scrapy_djangoitem import DjangoItem

class Tweet_item(DjangoItem):   # django item erstellen
    django_model = Tweets
    django_model2 = details

class Tweet(Item):
    id_ = Field()
    raw_data = Field()

class User(Item):
    id_ = Field()
    raw_data = Field()