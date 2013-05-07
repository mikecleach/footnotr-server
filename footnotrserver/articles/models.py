from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    def __unicode__(self):
        return self.title
        
    title = models.CharField(max_length=255)
    creator = models.ForeignKey('auth.User', related_name='articles')

class Annotation(models.Model):
    def __unicode__(self):
        string = self.xml + str(self.pdfLibID)
        return string
    
    article = models.ForeignKey(Article, related_name='annots')
    pdfLibID = models.IntegerField()
    xml = models.TextField()

class Comment(models.Model):
    def __unicode__(self):
        string = str(self.annotation.pdfLibID) + "  " + str(self.user) + "  " + self.comment
        return string
        
    annotation = models.ForeignKey(Annotation, related_name='comments')
    user = models.ForeignKey(User)
    comment = models.TextField()


class Vote(models.Model):
    comment = models.ForeignKey(Comment, related_name='votes')
    user = models.ForeignKey(User)
    
