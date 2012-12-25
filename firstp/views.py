from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse


def home(request):
    return render_to_response('firstp/index.html',context_instance=RequestContext(request))