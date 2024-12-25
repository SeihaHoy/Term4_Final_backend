from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import CV
from .serializer import CVSerializer
import joblib
import numpy as np
import cv2

@api_view(['GET'])
def cv_list(request):
    cv = CV.objects.all()
    serializer = CVSerializer(cv, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def cv_create(request):
    serializer = CVSerializer(data=request.data)
    if serializer.is_valid():
        cv_instance = serializer.save()
        response_data = serializer.data
        response_data['image_url'] = cv_instance.image.url
        response_data['image_pred_url'] = cv_instance.image.url
        return JsonResponse(response_data, status=201)
    return JsonResponse(serializer.errors, status=400)