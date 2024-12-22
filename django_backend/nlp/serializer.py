from rest_framework import serializers
from .models import NLP

class NLPSerializer(serializers.ModelSerializer):
    class Meta:
        model = NLP
        fields = (
            'id',
            'text',
            'array_1',
            'array_2',
        )