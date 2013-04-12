from django.core import serializers
from django.http import HttpResponse
from articles.models import Annotation
# Create your views here.

def annotations(request, article_id):
    data = serializers.serialize("json",[Annotation.objects.get(id=article_id)])
    return HttpResponse(data)