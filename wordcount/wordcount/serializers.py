from rest_framework import serializers

class WordCountSerializer(serializers.Serializer):
    url = serializers.URLField()
    word = serializers.CharField(max_length=100)
