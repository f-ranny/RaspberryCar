from django.shortcuts import render
from django.http import HttpResponse

from .hardware.motors import robot
import json
from django.views.decorators.csrf import csrf_exempt

from .hardware.camera import camera, output
from logging import warning

STATE = False


# Create your views here.
def index(request):
    global STATE
    if not STATE:
        camera.capture(output, format="mjpeg")
        STATE = True
    return render(request, 'riding/index.html', )


def stream(request):
    response = HttpResponse()
    response['Age'] = 0
    response['Cache-Control'] = 'no-cache, private'
    response['Pragma'] = 'no-cache'
    response['Content-Type'] = 'multipart/x-mixed-replace; boundary=FRAME'
    try:
        with output.condition:
            output.condition.wait()
            frame = output.frame
        response.write(b'--FRAME\r\n')
        response['Content-Type'] = 'image/jpeg'
        response['Content-Length'] = len(frame)
        response.write(frame)
        response.write(b'\r\n')
    except Exception as e:
        warning(
            'Removed streaming client %s: %s',
            request.get_host(), str(e))
    return response


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
