from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers
from articles.models import Article, Annotation, Comment, Vote

class UserSerializer(serializers.ModelSerializer):
    #articles = serializers.PrimaryKeyRelatedField(many=True)
    pk = serializers.Field()
    
    class Meta:
        model = User
        fields = ('pk', 'username')


class WritableVoteSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    username = serializers.Field(source='user.username')

    class Meta:
        model = Vote
        fields = ( 'user', 'comment', 'pk', 'username')
        #depth = 1


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field()
    user = UserSerializer(source='user')
    username = serializers.Field(source='user.username')
    
    class Meta:
        model = Vote
        fields = ('user', 'pk', 'username')
        #depth = 1


class WritableCommentSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    username = serializers.Field(source='user.username')
    
    class Meta:
        model = Comment
        fields = ('comment', 'votes', 'user', 'pk', 'annotation', 'username')
        
class CommentSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field()
    votes = VoteSerializer()
    username = serializers.Field(source='user.username')

    class Meta:
        model = Comment
        fields = ('comment', 'votes', 'username', 'pk')#) 'user', 'pk')        

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
        #depth = 3
    

  
