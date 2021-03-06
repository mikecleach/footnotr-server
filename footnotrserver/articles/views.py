import json
from django.http import Http404, HttpResponse
from articles.models import Article, Annotation, Comment, Vote
import logging
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from articles.serializers import ArticleSerializer, WritableArticleSerializer, UserSerializer, AnnotationSerializer, WritableAnnotationSerializer, CommentSerializer, VoteSerializer, WritableVoteSerializer, WritableCommentSerializer
from articles.permissions import IsCreatorOrReadOnly, IsUserOwnedOrReadOnly
from rest_framework import generics, permissions

#FIXME: Remove always True from IsCreatorOrReadOnly, add proper permissions back
class ArticleList(generics.ListAPIView):
	model = Article
	serializer_class = ArticleSerializer
	#permission_classes = ( IsCreatorOrReadOnly, )
	
	#def pre_save(self, obj):
		#obj.creator = self.request.user
	

class ArticleAdd(generics.CreateAPIView):
	model = Article
	serializer_class = WritableArticleSerializer
	#permission_classes = ( IsCreatorOrReadOnly,)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
	model = Article
	serializer_class = ArticleSerializer
	permission_classes = ( IsUserOwnedOrReadOnly,)
	lookup_field = ('guid') 
	 
	#def pre_save(self, obj):
		#obj.creator = self.request.user  
	
class UserCommentList(generics.ListAPIView):
	serializer_class = AnnotationSerializer

	def get_queryset(self):
		user_id = self.kwargs['pk']
		import pdb; pdb.set_trace()
		return Annotation.objects.all()

class AnnotationList(generics.ListCreateAPIView):
	model = Annotation
	serializer_class = AnnotationSerializer
	#permission_classes = ( IsCreatorOrReadOnly,)

class AnnotationAdd(generics.CreateAPIView):
	model = Annotation
	serializer_class = WritableAnnotationSerializer
	#permission_classes = ( IsCreatorOrReadOnly,)


class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
	model = Annotation
	serializer_class = AnnotationSerializer
	permission_classes = ( IsUserOwnedOrReadOnly,) 

class CommentList(generics.ListAPIView):
	model = Comment
	serializer_class = CommentSerializer
	#permission_classes = ( IsCreatorOrReadOnly,)

class CommentAdd(generics.CreateAPIView):
	model = Comment
	serializer_class = WritableCommentSerializer
	#permission_classes = ( IsCreatorOrReadOnly,)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
	model = Comment
	serializer_class = CommentSerializer
	permission_classes = ( IsUserOwnedOrReadOnly,) 


class VoteList(generics.ListAPIView):
	model = Vote
	serializer_class = VoteSerializer
	#permission_classes = ( IsCreatorOrReadOnly,)
	
	# def post(self, request, *args, **kwargs):
	#     #import pdb; pdb.set_trace()
	#     return self.create(request, *args, **kwargs)
	# 
	# def pre_save(self,obj):
	#     pass
	#     #import pdb; pdb.set_trace()
	#     #pass
	

class VoteAdd(generics.CreateAPIView):
	model = Vote
	serializer_class = WritableVoteSerializer
	#permission_classes = ( IsCreatorOrReadOnly,)


class VoteDetail(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
	model = Vote
	serializer_class = VoteSerializer
	permission_classes = ( IsUserOwnedOrReadOnly,) 
	  


class UserList(generics.ListAPIView):
	model = User
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	model = User
	serializer_class = UserSerializer  



import datetime
#For some reason, user_comment_list correctly uses AnnotationSerializer, including
#following the comments relationship and serializing comments correctly
#EXCEPT for datetime objects, which it does not serialize to primitives. So, this
#JSONencoder subclass handles datetime objs, and defers to its' parent class o.w.
class DateTimeJSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return obj.isoformat()
		else:
			return super(DateTimeJSONEncoder, self).default(obj)

@csrf_exempt
def user_comment_list(request, pk):
	data = {}
	#data['username'] = user.username
	annotations = []
	for comm in Comment.objects.filter(user=pk):
		#import pdb; pdb.set_trace()
		data['username'] = comm.user.username
		as_data = AnnotationSerializer(comm.annotation).data
		as_data.insert(as_data.__len__(),'comment',comm.comment)
		annotations.append(as_data)
	jsonOut = json.dumps(annotations, cls=DateTimeJSONEncoder)
	return HttpResponse(jsonOut)

@csrf_exempt
def user_comment_list_by_name(request, username):
	data = {}
	#data['username'] = user.username
	annotations = []
	#import pdb; pdb.set_trace()
	for comm in Comment.objects.filter(user__username=username):
		data['username'] = comm.user.username
		as_data = AnnotationSerializer(comm.annotation).data
		as_data.insert(as_data.__len__(),'comment',comm.comment)
		annotations.append(as_data)
	jsonOut = json.dumps(annotations, cls=DateTimeJSONEncoder)
	return HttpResponse(jsonOut)


@csrf_exempt
def latest_comment_list(request):
	data = {}
	#data['username'] = user.username
	annotations = []
	for comm in Comment.objects.order_by('created').reverse()[:5]:
		#import pdb; pdb.set_trace()
		data['username'] = comm.user.username
		as_data = AnnotationSerializer(comm.annotation).data
		as_data.insert(as_data.__len__(),'comment',comm.comment)
		as_data.insert(as_data.__len__(),'comments_username',comm.user.username)
		annotations.append(as_data)
	jsonOut = json.dumps(annotations, cls=DateTimeJSONEncoder)
	return HttpResponse(jsonOut)


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
