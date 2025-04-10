from rest_framework import serializers
from .models import Episode, Highlight, Predictions

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = "__all__"

class HighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlight
        fields = "__all__"

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predictions
        fields = "__all__"