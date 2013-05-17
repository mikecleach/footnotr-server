from django.contrib import admin
from articles.models import *

admin.site.register(Article)
admin.site.register(Annotation)
admin.site.register(Comment)
admin.site.register(Vote)