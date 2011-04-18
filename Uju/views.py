from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.
def home(request):
    return render_to_response('base.html',
        context_instance=RequestContext(request)
    )
