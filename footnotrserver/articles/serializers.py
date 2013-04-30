from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers
from articles.models import Article, Annotation, Comment

class UserSerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(many=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'articles')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field()
    comment = serializers.CharField()
    votes = serializers.IntegerField()
    user = serializers.Field(source='user.username')
    
    class Meta:
        model = Comment
        fields = ('comment', 'votes','url', 'user')

class AnnotationSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field()
    pdfLibID = serializers.IntegerField()
    xml = serializers.CharField()
    comments = CommentSerializer(source='comments')
    
    class Meta:
        model = Annotation
        #fields = ('pdfLibID', 'xml','url')
    


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    title = serializers.CharField(max_length=255)
    creator = serializers.Field(source='creator.username')
    #this might be permanent way to do this, but need to figure out
    #read-write concerns first
    #annots = HyperlinkedRelatedField(many=True, read_only=True,                                     view_name='annotation-detail')
    annots = AnnotationSerializer(source='annots')

    class Meta:
        model = Article
        #fields = ('creator', 'title', 'annots')
        
    

  
