import json
from django.http import Http404, HttpResponse
from articles.models import Article, Annotation, Comment, Vote
import logging
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from articles.serializers import ArticleSerializer, UserSerializer, AnnotationSerializer, CommentSerializer, VoteSerializer
from articles.permissions import IsCreatorOrReadOnly
from rest_framework import generics, permissions

#FIXME: Remove always True from IsCreatorOrReadOnly, add proper permissions back
class ArticleList(generics.ListCreateAPIView):
    model = Article
    serializer_class = ArticleSerializer
    permission_classes = ( IsCreatorOrReadOnly, )
    
    def pre_save(self, obj):
        obj.creator = self.request.user
    

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Article
    serializer_class = ArticleSerializer
    permission_classes = ( IsCreatorOrReadOnly,) 
     
    def pre_save(self, obj):
        obj.creator = self.request.user  
    
class AnnotationList(generics.ListCreateAPIView):
    model = Annotation
    serializer_class = AnnotationSerializer
    permission_classes = ( IsCreatorOrReadOnly,)


class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Annotation
    serializer_class = AnnotationSerializer
    permission_classes = ( IsCreatorOrReadOnly,) 

class CommentList(generics.ListCreateAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = ( IsCreatorOrReadOnly,)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = ( IsCreatorOrReadOnly,) 


class VoteList(generics.ListCreateAPIView):
    model = Vote
    serializer_class = VoteSerializer
    permission_classes = ( IsCreatorOrReadOnly,)
    
    def post(self, request, *args, **kwargs):
        #import pdb; pdb.set_trace()
        return self.create(request, *args, **kwargs)
    
    def pre_save(self,obj):
        pass
        #import pdb; pdb.set_trace()
        #pass
    


class VoteDetail(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    model = Vote
    serializer_class = VoteSerializer
    permission_classes = ( IsCreatorOrReadOnly,) 
      


class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer  


@csrf_exempt    
def article(request, article_id):
    logger = logging.getLogger()
    if request.method == 'POST':
        json_str = request.body
        article_info = json.loads(json_str)
        logger.info(article_info)
        
        article_tuple = Article.objects.get_or_create(id=article_info['articleId'])
        
        article = article_tuple[0]
        article.title = article_info['title']
        article.save()
        for key,annot in article_info['annots'].iteritems():
            annot_tuple = Annotation.objects.get_or_create(pdfLibID=key,article=article)
            an = annot_tuple[0]
            an.xml = annot['xmlStr']
            an.article = article
            an.save()
        return HttpResponse("Article saved.")
    else:
        data = {}
        article = Article.objects.get(id=article_id)
        art_info = {}
        art_info['articleId'] = article_id
        art_info['articleTitle'] = article.title
        data['articleInfo'] = art_info
        
        annots = {}
        comments = {}
        for an in article.annots.order_by('pdfLibID').all():
            annots[an.pdfLibID] = {'xmlStr': an.xml}
            comments_info = {}
            if an.comments.exists():
                for c in an.comments.all():
                    comm_detail = {'user':c.user.username, 'comment_text':c.comment, 'votes':c.votes} 
                    comments_info[c.pk] = comm_detail
                comments[an.pdfLibID] = comments_info
    
        data['annots'] = annots
        data['comments'] = comments

    
        jsonOut = json.dumps(data)
        return HttpResponse(jsonOut)
