from django.test import TestCase

from django.test import TestCase
from rest_framework.test import APIClient

class WordCountAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_wordcount_api(self):
        # Check that wordcount API returns correct number of words on site
        data = {'url': 'https://webscraper.io/test-sites/e-commerce/static', 'word': 'scraped'}
        response = self.client.post('/api/wordcount/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['word'], 'scraped')
        self.assertEqual(response.data['count'], 1)

    def test_exact_word_match_only(self):
        # Define test data with a word that doesn't exist in the provided URL
        data = {'url': 'https://webscraper.io/test-sites/e-commerce/static', 'word': 'scraper'}
        response = self.client.post('/api/wordcount/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['word'], 'scraper')
        self.assertEqual(response.data['count'], 6)

    def test_non_existent_word(self):
        # Define test data with a word that doesn't exist in the provided URL
        data = {'url': 'https://webscraper.io/test-sites/e-commerce/static', 'word': 'foo'}
        response = self.client.post('/api/wordcount/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['word'], 'foo')
        self.assertEqual(response.data['count'], 0)

    def test_invalid_url(self):
        # Check that endpoint raises error when accessing invalid url
        data = {'url': 'foobar', 'word': 'test'}
        response = self.client.post('/api/wordcount/', data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
