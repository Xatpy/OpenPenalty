from django.http import HttpResponse, Http404
from django.template import Template, Context
from django.template.loader import get_template
import datetime
from django.shortcuts import render

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render(request, 'time_plus.html', {'offset': offset, 'dt': dt})
    #try:
    #    offset = int(offset)
    #except ValueError:
    #    raise Http404()
    #dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    #assert True
    #html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    #return HttpResponse(html)