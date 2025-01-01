from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import CV
from .serializer import CVSerializer
import joblib
import numpy as np
import cv2
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import os
import pytesseract  # Import Tesseract OCR
from ultralytics import YOLO


# Load YOLO model
def load_yolo_model():
    model = YOLO("/usr/src/django_backend/cv/yolov8_100epv6.pt")  # Adjust path as necessary
    
    return model

# Detect text using YOLO
def detect_text_yolo(image, model):
    results = model(image)  # Run inference on the image
    boxes = []
    confidences = []

    for result in results:  # Iterate over results
        for detection in result.boxes.data.tolist():  # Convert detections to a list
            x1, y1, x2, y2, conf = detection[:5]  # Extract bounding box and confidence
            if conf > 0.3:  # Adjusted confidence threshold
                boxes.append([int(x1), int(y1), int(x2 - x1), int(y2 - y1)])  # x, y, width, height
                confidences.append(float(conf))

    return boxes, confidences
# Function to draw bounding boxes on the image
def draw_boxes(image, boxes, color=(0, 255, 0)):
    for box in boxes:
        x, y, w, h = box
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)  # Draw rectangle

def preprocess_image(image):
    """Preprocess image for better OCR performance."""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    enhanced_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # Binarization
    return enhanced_image
        
def capture_and_extract_text(image):
    model = load_yolo_model()
    frame = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)

    boxes, confidences = detect_text_yolo(frame, model)

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.3, nms_threshold=0.5)

    detected_texts = []

    if len(indices) > 0:
        for i in indices.flatten():
            box = boxes[i]
            x, y, w, h = box

            # Add padding
            padding = 5
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(frame.shape[1] - x, w + 2 * padding)
            h = min(frame.shape[0] - y, h + 2 * padding)

            # Crop and preprocess
            cropped_text_image = frame[y:y+h, x:x+w]
            preprocessed_image = preprocess_image(cropped_text_image)

            # OCR with custom configuration
            custom_config = '--psm 7'
            recognized_text = pytesseract.image_to_string(preprocessed_image, lang='Khmer', config=custom_config).strip()

            if recognized_text:
                detected_texts.append(recognized_text)
                print(f"Detected Text: {recognized_text}") 

            # Draw bounding box on the original frame (optional)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Encode the frame with detections as an image
    _, buffer = cv2.imencode('.jpg', frame)
    image_pred = ContentFile(buffer.tobytes(), name='image_pred.jpg')

    return image_pred, detected_texts

@api_view(['GET'])
def cv_list(request):
    cv = CV.objects.all()
    serializer = CVSerializer(cv, many=True)
    return JsonResponse(serializer.data, safe=False)


# @api_view(['POST'])
# def cv_create(request):
#     serializer = CVSerializer(data=request.data, files=request.FILES)
#     if serializer.is_valid():
#         cv_instance = serializer.save()
#         response_data = serializer.data
#         response_data['image_url'] = cv_instance.image.url
#         response_data['image_pred_url'] = cv_instance.image_pred.url
#         return JsonResponse(response_data, status=201)
#     print(serializer.errors)  # Log the errors to the console
#     return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def cv_create(request):
    if request.method == 'POST':
        print("Request POST data:", request.POST)
        print("Request FILES data:", request.FILES)
        
        if request.FILES.get('file'):
            image = request.FILES['file']

            # Process the image and extract text
            image_pred, detected_texts = capture_and_extract_text(image)

            # Ensure detected_texts are properly encoded
            detected_texts = [text.encode('utf-8').decode('utf-8') for text in detected_texts]

            cv = CV.objects.create(image=image, image_pred=image_pred, text=detected_texts)
            cv.save()

            return JsonResponse({
                'image': cv.image.url,
                'image_pred': cv.image_pred.url,
                'text': detected_texts
            }, status=201)
    return JsonResponse({'error': 'Invalid request'}, status=400)