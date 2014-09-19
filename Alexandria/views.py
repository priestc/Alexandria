from django.template.response import TemplateResponse

def publish_dialog(request):
    connections = [
        {'domain': 'bob.com', 'name': "Bob Franks", "id": 1},
        {'domain': 'george.com', 'name': "George Smith", "id": 2},
        {'domain': 'harry.com', 'name': "Harry Johnson", "id": 3},
        {'domain': 'william.com', 'name': "William Jones", "id": 4},
    ]
    return TemplateResponse(request, "publish_dialog.html", locals())
