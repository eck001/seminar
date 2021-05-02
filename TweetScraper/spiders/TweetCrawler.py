import re, json, logging
from urllib.parse import quote

from scrapy import http
from scrapy.spiders import CrawlSpider
from scrapy.core.downloader.middleware import DownloaderMiddlewareManager
from scrapy_selenium import SeleniumRequest, SeleniumMiddleware

from TweetScraper.items import Tweet, User
import datetime
from TweetScraper.items import Tweet_item


logger = logging.getLogger(__name__)
unternehmensname = input("Geben Sie den Unternehmensname ein = ")
schluessel_id = input("Bitte SchlüsselId eingeben =")       # eingabe von name für Strukturierung
                                                            # schluesselID notwendig um Tweets von Werbe Tweets zu trennen

class TweetScraper(CrawlSpider):
    name = 'TweetScraper'
    allowed_domains = ['twitter.com']
    benutzerId = ''


    def __init__(self, query=''):

        self.url = (
            f'https://api.twitter.com/2/search/adaptive.json?'
            f'include_profile_interstitial_type=1'
            f'&include_blocking=1'
            f'&include_blocked_by=1'
            f'&include_followed_by=1'
            f'&include_want_retweets=1'
            f'&include_mute_edge=1'
            f'&include_can_dm=1'
            f'&include_can_media_tag=1'
            f'&skip_status=1'
            f'&cards_platform=Web-12'
            f'&include_cards=1'
            f'&include_ext_alt_text=true'
            f'&include_quote_count=true'
            f'&include_reply_count=1'
            f'&tweet_mode=extended'
            f'&include_entities=true'
            f'&include_user_entities=true'
            f'&include_ext_media_color=true'
            f'&include_ext_media_availability=true'
            f'&send_error_codes=true'
            f'&simple_quoted_tweet=true'
            f'&query_source=typed_query'
            f'&pc=1'
            f'&spelling_corrections=1'
            f'&ext=mediaStats%2ChighlightedLabel'
            f'&count=20'
            f'&tweet_search_mode=live'
        )
        self.url = self.url + '&q={query}'
        self.query = query
        self.num_search_issued = 0
        # regex for finding next cursor
        self.cursor_re = re.compile('"(scroll:[^"]*)"')


    def start_requests(self):
        """
        Use the landing page to get cookies first
        """
        yield SeleniumRequest(url="https://twitter.com/explore", callback=self.parse_home_page)


    def parse_home_page(self, response):
        """
        Use the landing page to get cookies first
        """
        # inspect_response(response, self)
        self.update_cookies(response)
        for r in self.start_query_request():
            yield r


    def update_cookies(self, response):
        driver = response.meta['driver']
        try:
            self.cookies = driver.get_cookies()
            self.x_guest_token = driver.get_cookie('gt')['value']
            # self.x_csrf_token = driver.get_cookie('ct0')['value']
        except:
            logger.info('cookies are not updated!')

        self.headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'x-guest-token': self.x_guest_token,
            # 'x-csrf-token': self.x_csrf_token,
        }

        print('headers:\n--------------------------\n')
        print("Daten werden gespeichert")
        print('\n--------------------------\n')



    def start_query_request(self, cursor=None):
        """
        Generate the search request
        """
        if cursor:
            url = self.url + '&cursor={cursor}'
            url = url.format(query=quote(self.query), cursor=quote(cursor))
        else:
            url = self.url.format(query=quote(self.query))
        request = http.Request(url, callback=self.parse_result_page, cookies=self.cookies, headers=self.headers)
        yield request

        self.num_search_issued += 1
        if self.num_search_issued % 100 == 0:
            # get new SeleniumMiddleware            
            for m in self.crawler.engine.downloader.middleware.middlewares:
                if isinstance(m, SeleniumMiddleware):
                    m.spider_closed()
            self.crawler.engine.downloader.middleware = DownloaderMiddlewareManager.from_crawler(self.crawler)
            # update cookies
            yield SeleniumRequest(url="https://twitter.com/explore", callback=self.update_cookies, dont_filter=True)


    def parse_result_page(self, response):
        """
        Get the tweets & users & next request
        """
        # inspect_response(response, self)

        # handle current page
        data = json.loads(response.text)
        for item in self.parse_databreaches(data['globalObjects']['tweets']):
            yield item

        for item in self.parse_user_item(data['globalObjects']['users']):
            yield item

        # get next page
        cursor = self.cursor_re.search(response.text).group(1)
        for r in self.start_query_request(cursor=cursor):
            yield r




    def parse_user_item(self, items):                   #Durch Userinformationen wird benutzerId bestimmt
        for k, v in items.items():
            # assert k == v['id_str'], (k,v)
            user = User()
            user['id_'] = k
            user['raw_data'] = v
            daten = user['raw_data']
            benutzername = daten['screen_name']
            if (benutzername == unternehmensname):
                self.benutzerId=daten['id_str']
                return self.benutzerId
            yield user

    def parse_databreaches(self, items):        # alle relevanten infos für unser DjangoItem
        for k, v in items.items():              # aus dem tweetItem des Crawlers gewonnen
            # assert k == v['id_str'], (k,v)
            tweet = Tweet()
            user = User
            tweet['id_'] = k
            tweet['raw_data'] = v
            daten = tweet['raw_data']           # raw_date ist dictionary mit ensprechenden variablen nach daten
            id2 = schluessel_id                 #schlüssel
            id = str(daten['user_id'])          # aus daten werden die jeweiligen infos in variablen gespeichert
            worte_anzahl = len(re.findall(r'\w+', daten['full_text']))  # wortanzahl mit library bestimmen
            datum = daten['created_at'].split()[1] + " " + daten['created_at'].split()[2] + " " + daten['created_at'].split()[5]  # datum string aufsplitten um nur tag,monat,jahr zu erhalten
            date_time_obj = datetime.datetime.strptime(datum, '%b %d %Y')   # datum string als datetime object
            item = Tweet_item()                           # dem Tweet item werden die werte aus den Variablen übergeben
            item['userId'] = id
            item['unternehmensname'] = unternehmensname
            item['datum'] = date_time_obj.date()          # datetime object  als nur date object übergeben

            item['woerter'] = worte_anzahl
            item['schluesselId'] = id2
            yield item
