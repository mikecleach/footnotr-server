from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    pass

class Annotation(models.Model):
    def __unicode__(self):
        string = self.xml + self.pdfLibID
        return string
    
    article = models.ForeignKey(Article)
    pdfLibID = models.IntegerField()
    xml = models.TextField()

class Comment(models.Model):
    annotation = models.ForeignKey(Annotation)
    user = models.ForeignKey(User)
    comment = models.TextField()
    votes = models.IntegerField(default=0)

