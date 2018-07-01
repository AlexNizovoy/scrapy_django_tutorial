import json
from django.db import models


class ScrapyItem(models.Model):
    unique_id = models.CharField(max_length=100)
    data = models.TextField()

    @property
    def to_dict(self):
        return {
            'data': json.loads(self.data)
        }

    def __str__(self):
        return self.unique_id
