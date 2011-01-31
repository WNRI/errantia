from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import time

@csrf_exempt
def connect(request):
    return HttpResponse('[true, {"name": "%d"}]' % time.time())

@csrf_exempt
def create_channel(request):
    return HttpResponse('[true, {"history_size": 40}]')

@csrf_exempt
def subscribe(request):
    return HttpResponse('[true, {}]')

@csrf_exempt
def publish(request):
    return HttpResponse('[true, {}]')
