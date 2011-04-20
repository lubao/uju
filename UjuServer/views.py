from django.template import RequestContext
from django.shortcuts import render_to_response
from Gammu.models import Inbox, SentItems
# Create your views here.
def home(request):
    sent_items = SentItems.objects.all()
    inbox = Inbox.objects.all()
    return render_to_response('UjuServer/home.html',
        {'sent_items':sent_items,'inbox':inbox,},
        context_instance=RequestContext(request)
    )
