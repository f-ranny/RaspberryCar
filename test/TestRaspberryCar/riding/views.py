from django.shortcuts import render
from django.http import HttpResponse
from .hardware.motors import robot
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return render(request, 'riding/index.html')


@csrf_exempt
def motors(request):
    content_length = int(request.headers['Content-Length'])
    body = request.read(content_length)

    data_dict = json.loads(body.decode('utf-8'))

    if data_dict['direction'] == 1:
        robot.forward()
    elif data_dict['direction'] == 2:
        robot.backward()
    elif data_dict['direction'] == 3:
        robot.right()
    elif data_dict['direction'] == 4:
        robot.left()
    else:
        robot.stop()

    return HttpResponse(b'OK')
