import datetime
import hashlib

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpRespone
from django.conf import settings

from models import LibraryUser, LibraryItem

CONNECTIONS = [
        {
            'domain': 'obama.com',
            'name': "Barak Obama",
            "id": 1,
            'avatar': 'http://www.elrst.com/wp-content/uploads/2012/11/US-President-Barack-Obama.jpg'
        },
        {
            'domain': 'georgebush.com',
            'name': "George Bush",
            "id": 2,
            'avatar': 'https://lh4.googleusercontent.com/-B1n8Cn3iaUc/UEBCQKprgwI/AAAAAAAAAG4/Xdc01Mx7NzE/bush.jpg'
        },
        {
            'domain': 'clinton.com',
            'name': "Bill Clinton",
            "id": 3,
            'avatar': 'https://38.media.tumblr.com/avatar_1f95d9bd9fa2_128.png'
        },
        {
            'domain': 'reagan.com',
            'name': "Ronald Reagan",
            "id": 4,
            'avatar': 'http://www.headlinepolitics.com/wp-content/uploads/2014/09/1reagan-128x128.jpg'
        },
    ]


def view_connections(request):
    connections = CONNECTIONS
    return TemplateResponse(request, "connections.html", locals())

@user_passes_test(lambda u: u.is_superuser)
def append_transfer_query(request):
    """
    API end point for appending onto a connection's transfer query.
    """
    domain = request.POST['domain']
    query = request.POST['query']
    
    library = RemoteLibraryUser.objects.get(domin=domain)
    library.transfer_query += query
    library.save()
    
    return HttpResponse("OK")

def query(request):
    """
    API endpoint for returning Library Items. These requests can come in from anywhere.
    Either a device owned by the Library owner, or another Library.
    """
    origin = (request.user and request.user.username) or ''
    query = request.GET['query']
        
    return JsonResponse(LibraryItem.objects.dicts_from_lql(origin, query))
    

@user_passes_test(lambda u: u.is_superuser)
def publish(request):
    """
    API endpoint for adding a new publication. This view can only be accessed by
    clients that have publish permissions (superusers).
    """
    request.user
    

def request_authorization(request):    
    """
    API endpoint for other libraries to call when they are connecting to this
    library. Will always be a POST request.
    """
    requested_transfer_query = request.POST.get('transfer_query', '')
    domain = request.POST['domain']
    library, created = LibraryUser.objects.get_or_create(domain=domain)
    
    if created:
        library.set_password(request.POST['password'])
        user = authenticate(username=domain, password=password)
    else:
        user = authenticate(username=domain, password=password)
        
    if not user:
        return HttpResponse("invalid credentials", code=401)
        
    if requested_transfer_query:
        PendingAuthorization.objects.create(
            library=library,
            query_to_be_added=requested_transfer_query
        )
    
    login(request, user)
    
    return HttpResponse("OK")


@user_passes_test(lambda u: u.is_superuser)
def publish_dialog(request):
    connections = CONNECTIONS
    
    metadata = [
        {
            'key': 'hash',
            'value': hashlib.sha256(b'dsfsdfsdf').hexdigest(),
            'editable': False,
        },
        {
            'key': 'origin',
            'value': 'chrispriest.pw',
            'editable': False,
        },
        {
            'key': 'date_published',
            'value': datetime.datetime.now().isoformat(),
            'editable': False,
        },
        {
            'key': 'mimetype',
            'value': 'text/plain',
            'editable': False,
        },
        {
            'key': 'title',
            'value': '',
            'editable': True,
        }
    ]
    
    return TemplateResponse(request, "publish_dialog.html", locals())
