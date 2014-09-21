import datetime

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
import arrow
import requests

class RemoteLibraryUser(AbstractBaseUser):
    """
    Represents another library that wants content from this library.
    If transfer_query is blank, they only see public items.
    """
    domain = models.CharField(max_length=40, unique=True)
    transfer_query = models.TextField(blank=True)
    
    USERNAME_FIELD = 'domain'

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

class RemoteLibrary(models.Model):
    """
    Represents a remote library that this user wants to connect to. Slightly
    different than the model above. Each library in this table has a corresponding
    LibraryUser instance on /that/ library.
    """
    domain = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=64)

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

class PendingAuthorization(modes.Model):
    """
    Represents an addition to a library's Transfer Query.
    """
    library = models.ForeignKey(LibraryUser)
    issued = models.DateTimeField(default=datetime.datetime.now)
    query_to_be_added = models.TextField()
