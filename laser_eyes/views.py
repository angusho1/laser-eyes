from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import base64
from .services import apply_lasers, detect_eyes
import numpy
import cv2
import json

from django.http import Http404, HttpResponse, HttpRequest, JsonResponse, FileResponse

def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')

@csrf_exempt
def detect(request: HttpRequest) -> JsonResponse:
    files = request.FILES.getlist('image')
    img_file = files[0]

    # Ref: https://stackoverflow.com/questions/27517688/can-an-uploaded-image-be-loaded-directly-by-cv2
    cv2_img = cv2.imdecode(numpy.fromstring(img_file.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

    detected_faces = detect_eyes(cv2_img)

    return JsonResponse(detected_faces, safe=False)

@csrf_exempt
def apply(request: HttpRequest) -> HttpResponse:
    files = request.FILES.getlist('image')
    detected_faces = json.loads(request.POST['faces'])
    laser_scale = request.POST['laserScale']
    img_file = files[0]

    cv2_img = cv2.imdecode(numpy.fromstring(img_file.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    image_result = apply_lasers(cv2_img, detected_faces, laser_scale)

    # Ref: https://stackoverflow.com/questions/17967320/python-opencv-convert-image-to-byte-string
    img_bytes = cv2.imencode('.jpg', image_result)[1].tostring()
    img_b64_encoded = base64.b64encode(img_bytes)

    return HttpResponse(img_b64_encoded, content_type='image/jpeg')