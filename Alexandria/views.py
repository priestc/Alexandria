import datetime
import hashlib

from django.template.response import TemplateResponse

def publish_dialog(request):
    connections = [
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
    
    metadata = [
        {
            'key': 'hash',
            'value': hashlib.sha256(b'dsfsdfsdf').hexdigest(),
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
