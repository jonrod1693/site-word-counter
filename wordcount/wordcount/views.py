from bs4 import BeautifulSoup
from rest_framework import generics
from rest_framework.response import Response

import re
import requests

from .serializers import WordCountSerializer

class WordCountAPIView(generics.CreateAPIView):
    def post(self, request):
        serializer = WordCountSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            word = serializer.validated_data['word']

            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser', from_encoding=response.apparent_encoding)
                [s.extract() for s in soup(['head', 'title', 'meta', 'style', 'script', '[document]'])]
                page_text = soup.get_text()
                pattern = r'\b{}\b'.format(re.escape(word))
                word_count = len(re.findall(pattern, page_text.lower()))

                return Response({'word': word, 'count': word_count})
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        else:
            return Response({'error': str(serializer.errors)}, status=400)
