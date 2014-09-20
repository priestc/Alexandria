from django.db import models
import requests

def make_remote_library_query(domain, lql):
    """
    Send a query to a library. This sunction handles setting all appropriate
    headers an 
    """
    useragent = 'Alexandria-Beta (%s)' % settings.MY_LIBRARY_DOMAIN
    
    return requests.get(
        "https://" + domain + "/api/query",
        params={'query': lql},
        headers={'User-Agent': useragent}
    )


CURRENCIES = ((1, 'BTC'), (2, 'LTC'))

class MetaDataPair(models.Model):
    key = models.TextField()
    value_str = models.TextField()
    value_numeric = models.FloatField(null=True)
    value_date = models.DateTimeField(null=True)
    item = models.ForeignKey('Alexandria.LibraryItem')
    
class LibraryItem(models.Model):
    hash = models.CharField(max_length=64)
    origin = models.CharField(max_length=128)
    price_currency = models.IntegerField(choices=CURRENCIES)
    price_amount = models.FloatField(default=0)

    def set_metadata(self, metadata):
        for key, value in metadata:
            try:
                as_date = arrow.get(value).datetime
            except arrow.parser.ParserError:
                as_date = None
            
            try:
                as_number = float(vaue)
            except ValueError:
                as_number = None
            
            MetaDataPair.objects.create(
                value_str=value,
                value_date=as_date,
                value_numeric=as_number,
                key=key,
                item=self,
            )

class RemoteLibrary(models.Model):
    domain = models.TextField()
    transfer_query = models.TextField()
    
    def __str__(self):
        return self.domain
        
    def get_info(self):
        """
        Make a request to this remote library, make a query for the published
        library info, then return details (for now just full name and avatar)
        """
        response = make_remote_library_query(self.domain, "INCLUDING mimetype='library/info'")
        latest = response[0]
        return latest['real_name'], latest['avatar']
        
    def get_items(self, query):
        return make_remote_library_query(self.domain, query)
