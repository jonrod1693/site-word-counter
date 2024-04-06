from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

import re
import requests

from .models import SiteWordCount
from .serializers import WordCountSerializer

class WordCountAPIView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = WordCountSerializer

    def post(self, request):
        """
        Returns word and word count in json format.
        """
        serializer = self.serializer_class(data=request.data)
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

                record, created = SiteWordCount.objects.update_or_create(
                    url=url,
                    word=word,
                    defaults={'count': word_count}
                )

                return Response({'word': record.word, 'count': record.count})
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        else:
            return Response({'error': str(serializer.errors)}, status=400)
