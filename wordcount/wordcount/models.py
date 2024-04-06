from django.db import models

class SiteWordCount(models.Model):
    url = models.URLField()
    word = models.CharField(max_length=100)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.url} - {self.word} - {self.count}"
