from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
    # t = loader.get_template('todos/index.html')
    # c = Context({
    #   'latest_poll_list': 'sdasd',
    # })
    return render_to_response('todos/index.html',context_instance=RequestContext(request))