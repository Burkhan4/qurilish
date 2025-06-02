from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Term(models.Model):
    word = models.CharField(max_length=100)
    definition = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='terms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word
