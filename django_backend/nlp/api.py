from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import NLP
from .serializer import NLPSerializer
import joblib 
import numpy as np


CRF_MODEL_PATH = "/usr/src/django_backend/nlp/crf_model.pkl"
crf = joblib.load(CRF_MODEL_PATH)

def word2features(sentence, i):
    """
    Extract features for the i-th word in a sentence.
    """
    word = sentence[i]
    features = {
        'word.lower()': word.lower(), # Lowercase version of the word
        'word.isupper()': word.isupper(), # Is the word in all uppercase?
        'word.istitle()': word.istitle(), # Is the first letter capitalized?
        'word.isdigit()': word.isdigit(), # Is the word a number?
    }
    
    # Add features for previous word
    if i > 0:
        prev_word = sentence[i - 1]
        features.update({
            '-1:word.lower()': prev_word.lower(), # Lowercase version of the previous word
            '-1:word.isupper()': prev_word.isupper(),
            '-1:word.istitle()': prev_word.istitle(),
            '-1:word.isdigit()': prev_word.isdigit(),
        })
    else:
        features['BOS'] = True  # Beginning of Sentence
    
    # Add features for next word
    if i < len(sentence) - 1:
        next_word = sentence[i + 1]
        features.update({
            '+1:word.lower()': next_word.lower(),
            '+1:word.isupper()': next_word.isupper(),
            '+1:word.istitle()': next_word.istitle(),
            '+1:word.isdigit()': next_word.isdigit(),
        })
    else:
        features['EOS'] = True  # End of Sentence
    
    return features
def extract_features_for_sentence(sentence):
    """
    Extract features for all words in a sentence.
    """
    return [word2features(sentence, i) for i in range(len(sentence))]

@api_view(['GET'])
def nlp_list(request):
    nlp = NLP.objects.all()
    serializer = NLPSerializer(nlp, many=True)
    return JsonResponse(serializer.data, safe=False)

# #create a post request
# @api_view(['POST'])
# def nlp_create(request):
#     serializer = NLPSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def nlp_create(request):
    """
    Handle POST requests to process text, predict tags using the CRF model, and save to the database.
    """
    try:
        # Get the text from the request
        text = request.data.get("text", "")
        if not text:
            return Response({"error": "Text is required"}, status=400)

        # Preprocess the text
        new_sentence = text.split(" ")

        # Extract features for the sentence
        new_sentence_features = extract_features_for_sentence(new_sentence)

        # Predict tags for the sentence
        predicted_tags = crf.predict([new_sentence_features])[0]

        # Convert predicted tags to a Python list if needed
        if isinstance(predicted_tags, np.ndarray):
            predicted_tags = predicted_tags.tolist()

        # Save the results to the database
        nlp_instance = NLP.objects.create(
            text=text,
            array_1=new_sentence,  # Store the words
            array_2=predicted_tags  # Store the tags
        )

        # Create a proper JSON response
        response_data = {
            "text": nlp_instance.text,
            "array_2": nlp_instance.array_2
        }

        return JsonResponse(response_data, safe=False)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
