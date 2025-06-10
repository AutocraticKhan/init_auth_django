from django.contrib import admin
from .models import Review, Bookmark, Question, Answer, Report, ReviewPhoto

# Register your models here.
admin.site.register(Review)
admin.site.register(Bookmark)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Report)
admin.site.register(ReviewPhoto)
