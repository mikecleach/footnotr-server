import json
from django.http import HttpResponse
from articles.models import Article, Annotation, Comment
import logging
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
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