from django.db import models
from account.models import User
from django.utils.text import slugify
# Create your models here.

class Topic(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	name=models.CharField(max_length=50, unique=True, blank=False, null=False)
	description = models.TextField(blank=False, null=False)
	created = models.DateTimeField(auto_now_add=True, auto_created=True)
	updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.name


class Question(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	topic = models.ManyToManyField(Topic,blank=True,related_name="topics")
	question=models.CharField(max_length=400, null=False, blank=False)
	description=models.TextField(null=False, blank=False)
	keywords = models.CharField(max_length=255 ,blank=True)
	views=models.IntegerField(default=0)
	answers=models.IntegerField(default=0)
	answered=models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True, auto_created=True)
	updated = models.DateTimeField(auto_now=True, auto_created=True)
	url= models.SlugField(max_length=500, unique=True, blank=True, editable=False)
	
	def save(self, *args, **kwargs):
		self.url = self.question
		self.url= slugify(self.url)
		super(Question, self).save(*args, **kwargs)

	def __str__(self):
		return self.question

class Answer(models.Model):
	question = models.ForeignKey(Question,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	answer=models.TextField()
	votes=models.IntegerField(default=0)
	accepted=models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True, auto_created=True)
	updated = models.DateTimeField(auto_now=True, auto_created=True)

	def __str__(self):
		return self.answer

class AnswerComment(models.Model):
#	question = models.ForeignKey(Question,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	body=models.TextField(null=False,blank=False)
	question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE, related_name="comment_answer")
	replied_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="answer_replied")
	created = models.DateTimeField(auto_now_add=True, auto_created=True)
	updated = models.DateTimeField(auto_now=True, auto_created=True)
	def __str__(self):
		return self.body

class QuestionComment(models.Model):
#	question = models.ForeignKey(Question,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	body=models.TextField(null=False,blank=False)
	question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
	replied_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="question_replied")
	created = models.DateTimeField(auto_now_add=True, auto_created=True)
	updated = models.DateTimeField(auto_now=True, auto_created=True)
	def __str__(self):
		return self.body

class Vote(models.Model):
	question = models.ForeignKey(Question,on_delete=models.DO_NOTHING)
	answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	vote=models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True, auto_created=True)
	def __str__(self):
		return str(self.vote)

class Like(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	answer = models.ForeignKey(AnswerComment, null=True, blank=True, default=0, on_delete=models.CASCADE)
	question = models.ForeignKey(QuestionComment, null=True, blank=True, default=0, on_delete=models.CASCADE)
	like = models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True, auto_created=True)
	def __str__(self):
		return str(self.like)