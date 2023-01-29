from django.contrib import admin

from question.models import Topic, AnswerComment, Answer, Question, QuestionComment, Vote, Like

admin.site.register(Question)
admin.site.register(Topic)
admin.site.register(QuestionComment)
admin.site.register(AnswerComment)
admin.site.register(Answer)
admin.site.register(Vote)
admin.site.register(Like)