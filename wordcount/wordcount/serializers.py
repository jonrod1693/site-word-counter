from rest_framework import serializers

class WordCountSerializer(serializers.Serializer):
    url = serializers.URLField(help_text='Valid URL of website to count given word for.')
    word = serializers.CharField(max_length=100, help_text='Word to match in website URL, max of 100 characters.')
