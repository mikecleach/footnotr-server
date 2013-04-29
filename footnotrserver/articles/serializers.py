from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers
from articles.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    title = serializers.CharField(max_length=255)
    creator = serializers.Field(source='creator.username')

    class Meta:
        model = Article
        fields = ('creator',
                  'title')
        

class UserSerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'articles')