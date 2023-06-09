from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import User
from .forms import FormAnswer,FormAnswerComment,FormLike,FormQuestion,FormQuestionComment,FormTopic,FormVote
from question.models import Question, Answer, Vote,AnswerComment,QuestionComment, Like
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.

@login_required(redirect_field_name='next', login_url=None)
def Question_create(request):
  top = Question.objects.filter().order_by('-views')[:5]
  if request.user.is_authenticated:
    profile = get_object_or_404(User,username=request.user)
    if profile.points < 100:
      val = str(profile.points)+" / 100"
      percent = float(profile.points)/100*100
    elif profile.points < 1000:
      val = str(profile.points)+" / 1000"
      percent = float(profile.points)/1000*100
    elif profile.points < 2000:
      val = str(profile.points)+" / 2000"
      percent = float(profile.points)/2000*100
    else:
      val = str(profile.points)
      percent = 100
  else:
    profile = get_object_or_404(User,id=1)
    val = ""
    percent = 100


  if request.method == 'POST':
    question = request.POST['question']
    des = request.POST['description']
    user = request.user
    instance=get_object_or_404(User,username=user)
    ques = Question(user=instance,question=question, description=des)
    ques.save()
    instance.points = instance.points + 2
    instance.questions = instance.questions+1
    instance.save()
    messages.success(request, "Question Submitted.")
    return HttpResponseRedirect('/')
  form = FormQuestion()
  context={
    "form": form,
    "value":"",
    "description":"",
    "action":"/create/",
    "profile":profile,
    "val":val,
    "percent":percent,
    "q":Question.objects.count(),
    "a":Answer.objects.count(),
    "u":User.objects.filter(Q(is_staff=False) | Q(is_superuser=False)).count(),
    "top":top
  }
  return render(request,"question/create.html",context)

@login_required(redirect_field_name='next', login_url=None)
def Question_update(request, id,url):
  instance=get_object_or_404(Question,id=id)
  form = FormQuestion(instance=instance)
#  print(form)  
  if request.user == instance.user:
    top = Question.objects.all().order_by('-views')[:5]
    if request.user.is_authenticated:
      profile = get_object_or_404(User,username=request.user)
      if profile.points < 100:
        val = str(profile.points)+" / 100"
        percent = float(profile.points)/100*100
      elif profile.points < 1000:
        val = str(profile.points)+" / 1000"
        percent = float(profile.points)/1000*100
      elif profile.points < 2000:
        val = str(profile.points)+" / 2000"
        percent = float(profile.points)/2000*100
      else:
        val = str(profile.points)
        percent = 100
    else:
      profile = get_object_or_404(User,id=1)
      val = ""
      percent = 100
    
    if request.method == 'POST':
      form = FormQuestion(request.POST, instance=instance)
      if form.is_valid():
        form.save()
        messages.success(request, "Question Updated.")
        return redirect(reverse('detail', kwargs={'id':id,'url':url}))
    x="/update/" + str(id) + "/" + url + "/"
    context={
      "form": form,
      "value":instance.question,
      "description":instance.description,
      "action":x,
      "profile":profile,
      "val":val,
      "percent":percent,
      "q":Question.objects.count(),
      "a":Answer.objects.count(),
      "u":User.objects.filter(Q(is_staff=False) | Q(is_superuser=False)).count(),      
      "top":top
    }
    return render(request,"question/create.html",context)
  else:
    messages.error(request, "User unauthorized.")
    return HttpResponseRedirect('/')

@login_required(redirect_field_name='next', login_url=None)
def Answer_update(request, id):
  instance=get_object_or_404(Answer,id=id)
  if request.user == instance.user:
    top = Question.objects.all().order_by("-views")[:5]
    if request.user.is_authenticated:
      profile = get_object_or_404(User,username=request.user)
      if profile.points < 100:
        val = str(profile.points)+" / 100"
        percent = float(profile.points)/100*100
      elif profile.points < 1000:
        val = str(profile.points)+" / 1000"
        percent = float(profile.points)/1000*100
      elif profile.points < 2000:
        val = str(profile.points)+" / 2000"
        percent = float(profile.points)/2000*100
      else:
        val = str(profile.points)
        percent = 100
    else:
      profile = get_object_or_404(User,id=1)
      val = ""
      percent = 100
    
    form = FormAnswer(instance=instance)
    
    if request.method == 'POST':
      answer = FormAnswer(request.POST, instance=instance)
      if answer.is_valid():
        instance = answer.save(commit=False)
        instance.updated = datetime.now()
        instance.save()
        return redirect('detail',id=instance.question.id,url=instance.question.url)        
      else:
        messages.success(request, "Answer not Updated.")
        return redirect('ans_update',id=id)
    context={
      "form":form,
      "profile":profile,
      "val":val,
      "percent":percent,
      "q":Question.objects.count(),
      "a":Answer.objects.count(),
      "u":User.objects.filter(Q(is_staff=False) | Q(is_superuser=False)).count(),    
      "top":top
    }
    return render(request,"question/ans_update.html",context)
  else:
    messages.error(request, "User unauthorized.")
    return HttpResponseRedirect('/')

@login_required(redirect_field_name='next', login_url=None)
def Answer_delete(request,id):
  instance=get_object_or_404(Answer,id=id)
  if request.user == instance.user:
    instance.question.answers = instance.question.answers-1
    instance.question.save()
    instance.accepted = 0
    instance.save()
    if Answer.objects.filter(question=instance.question, accepted=1).exists():
      instance.question.answered = 1
    else:
      instance.question.answered = 0
    instance.question.save()
    instance.user.answers = instance.user.answers - 1
    instance.user.save()
    instance.delete()
    messages.success(request, "Successfully deleted")
  return HttpResponseRedirect('/')

@login_required(redirect_field_name='next', login_url=None)
def Answer_accept(request,id=None):
  instance=get_object_or_404(Answer,id=id)
  if request.user == instance.question.user.user:
    instance.accepted = 1
    instance.user.points = instance.user.points + 10
    instance.user.save()
    instance.save()
    instance.question.answered = 1
    instance.question.save()
    return HttpResponseRedirect('/question/'+str(instance.question.id)+'/'+instance.question.url+'/')
  else:
    messages.error(request, "User unauthorized.")
    return HttpResponseRedirect('/question/'+str(instance.question.id)+'/'+instance.question.url+'/')

@login_required(redirect_field_name='next', login_url=None)
def vote_up(request,id,url):
  question = get_object_or_404(Question,url=url)
  instance=get_object_or_404(Answer,id=id)
  if Vote.objects.all().filter(answer=instance, user=request.user).exists():
    vote = get_object_or_404(Vote,answer=instance, user=request.user)
    if vote.vote==-1:
      instance.votes = instance.votes+2
      instance.save()
      vote.vote = 1
      vote.question = question
      vote.save()
      return HttpResponseRedirect('/question/'+str(instance.question.id)+'/'+url+'/')
    else:
      messages.error(request, "Already voted up")
      return HttpResponseRedirect('/question/'+str(instance.question.id)+'/'+url+'/')
  else:

    vote = Vote(answer=instance, user=request.user,vote=1)
    instance.votes = instance.votes+1
    instance.save()
    vote.question = question    
    vote.save()
    return HttpResponseRedirect('/question/'+str(instance.question.id)+'/'+url+'/')

@login_required(redirect_field_name='next', login_url=None)
def vote_down(request,id,url):
  instance=get_object_or_404(Answer,id=id)
  question = get_object_or_404(Question,url=url)      
  if Vote.objects.filter(answer=instance, user=request.user).exists():
    vote = get_object_or_404(Vote,answer=instance, user=request.user)
    if vote.vote==1:
      instance.votes = instance.votes-2
      instance.save()
      vote.vote = -1
      vote.question = question      
      vote.save()
      return HttpResponseRedirect('/question/'+str(instance.question.id)+'/'+url+'/')
    else:
      messages.error(request, "Already voted down")
      return HttpResponseRedirect('/question/'+str(instance.question.id)+'/'+url+'/')
  else:
    vote = Vote(answer=instance, user=request.user,vote=-1)
    instance.votes = instance.votes-1
    instance.save()
    vote.question = question    
    vote.save()
    return HttpResponseRedirect('/question/'+str(instance.question.id)+'/'+url+'/')

@login_required(redirect_field_name='next', login_url=None)
def Answer_unaccept(request,id):
  instance=get_object_or_404(Answer,id=id)
  if request.user == instance.question.user.user:
    instance.accepted = 0
    instance.user.points = instance.user.points - 10
    instance.user.save()
    instance.save()
    if Answer.objects.filter(question=instance.question, accepted=1).exists():
      instance.question.answered = 1
    else:
      instance.question.answered = 0
    instance.question.save()
    return HttpResponseRedirect('/question/'+str(instance.question.id)+'/'+instance.question.url+'/')
  else:
    messages.error(request, "User unauthorized.")
    return HttpResponseRedirect('/question/'+str(instance.question.id)+'/'+instance.question.url+'/')

def Question_detail(request,id,url):
  top = Question.objects.filter().order_by('-views')[:5]
  if request.user.is_authenticated:
    profile = get_object_or_404(User,username=request.user)
    if profile.points < 100:
      val = str(profile.points)+" / 100"
      percent = float(profile.points)/100*100
    elif profile.points < 1000:
      val = str(profile.points)+" / 1000"
      percent = float(profile.points)/1000*100
    elif profile.points < 2000:
      val = str(profile.points)+" / 2000"
      percent = float(profile.points)/2000*100
    else:
      val = str(profile.points)
      percent = 100
  else:
    profile = get_object_or_404(User,id=1)
    val = ""
    percent = 100
  instance=get_object_or_404(Question,id=id,url=url)
  question = instance
  instance.views = instance.views + 1
  instance.save()

  vote = Vote.objects.filter(question=instance)
  question_comments=QuestionComment.objects.filter(question=instance).order_by("created","updated","like")
  answers_comments=AnswerComment.objects.filter(question=instance).order_by("created","updated","like")
  queryset=Answer.objects.all().filter(question=instance).order_by("-accepted","-votes","-created",'-updated')

  if request.method == 'POST':
    if request.user.is_authenticated:
      if 'comment_question' in request.POST and 'comment_question' != '':
        comment = request.POST['comment_question']
        replied_to = request.POST['replied_to']
        replied_to = get_object_or_404(User,id=replied_to)
        instance=get_object_or_404(User,username=request.user)
        ans=QuestionComment(body=comment, question=question, user=instance, replied_to=replied_to)
        instance.save()
        question.save()
        ans.save()
        return HttpResponseRedirect('/question/'+str(id)+'/'+str(url)+'/')

      elif 'answer' in request.POST and 'answer' != '':
        comment = request.POST['answer']
        instance=get_object_or_404(User,username=request.user)
        ans=Answer(answer=comment, question=question, user=instance)
        question.answers = question.answers+1
        instance.points = instance.points + 1
        instance.answers = instance.answers + 1
        instance.save()
        question.save()
        ans.save()
        return HttpResponseRedirect('/question/'+str(id)+'/'+str(url)+'/')
      
      elif 'comment_answer' in request.POST and 'comment_answer' != '':
        comment = request.POST['comment_answer']
        replied_to = request.POST['replied_to']
        replied_answer = request.POST['replied_answer']        
        replied_answer = get_object_or_404(Answer,answer=replied_answer)
        replied_to = get_object_or_404(User,id=replied_to)
        instance=get_object_or_404(User,username=request.user)
        ans=AnswerComment(body=comment, question=question, answer=replied_answer, user=instance, replied_to=replied_to)
        instance.save()
        question.save()
        ans.save()
        return HttpResponseRedirect('/question/'+str(id)+'/'+str(url)+'/')
    else:
      messages.error(request, "Please log in to answer.")
      return HttpResponseRedirect('/login/')


  context={
    "vote":vote,
    "question":question,
    "object_list":queryset,
    "comments_q":question_comments,
    "comments_a":answers_comments,
    "page":"page",
    "profile":profile,
    "val":val,
    "percent":percent,
    "q":Question.objects.count(),
    "a":Answer.objects.count(),
    "u":User.objects.filter(Q(is_staff=False) | Q(is_superuser=False)).count(),
    "top":top
  }
  return render (request,"question/question.html",context)

@login_required(redirect_field_name='next', login_url=None)
def Question_list(request):
  top = Question.objects.filter().order_by('-views')[:5]
  profile = {}
  if request.user.is_authenticated:
    profile = get_object_or_404(User,username=request.user)
  queryset_list=Question.objects.all().order_by("-created","-updated",)
  queryset_list_home=Question.objects.all().order_by("-views","-created","-updated",)
  query=request.GET.get('q')
  if query:
    queryset_list=queryset_list.filter(
    Q(question__icontains=query)|
    Q(description__icontains=query)|
    Q(user__username__icontains=query)
    ).distinct()
  else:
    query = ''
  paginator = Paginator(queryset_list, 10)
  page = request.GET.get('page')
  try:
    queryset_list = paginator.page(page)
    queryset_list_home = paginator.page(page)    
  except PageNotAnInteger:
    queryset_list = paginator.page(1)
    queryset_list_home = paginator.page(1)    
  except EmptyPage:
    queryset_list = paginator.page(paginator.num_pages) 
    queryset_list_home = paginator.page(paginator.num_pages)    

  username='Login'
  if User.is_active:
    username = User.username
  context={
    "query":query,
    "object_list":queryset_list,
    "object_list_home":queryset_list_home,
    "username":username,
    "profile":profile,
    "q":Question.objects.count(),
    "a":Answer.objects.count(),
    "u":User.objects.filter(Q(is_staff=False) | Q(is_superuser=False)).count(),
    "top":top
  }
  return render(request,"question/index.html",context)

@login_required(redirect_field_name='next', login_url=None)
def Question_list_views(request):
  top = Question.objects.filter().order_by('-views')[:5]
  if request.user.is_authenticated:
    profile = get_object_or_404(User,username=request.user)
    if profile.points < 100:
      val = str(profile.points)+" / 100"
      percent = float(profile.points)/100*100
    elif profile.points < 1000:
      val = str(profile.points)+" / 1000"
      percent = float(profile.points)/1000*100
    elif profile.points < 2000:
      val = str(profile.points)+" / 2000"
      percent = float(profile.points)/2000*100
    else:
      val = str(profile.points)
      percent = 100
  else:
    profile = get_object_or_404(User,id=1)
    val = ""
    percent = 100
  queryset_list=Question.objects.all().order_by("-views")
  query=request.GET.get('q')
  if query:
    queryset_list=queryset_list.filter(
    Q(question__icontains=query)|
    Q(description__icontains=query)|
    Q(user__user__username__icontains=query)
    ).distinct()
  paginator = Paginator(queryset_list, 10)
  page = request.GET.get('page')
  username='Login'
  if User.is_active:
    username = User.username
  try:
    queryset = paginator.page(page)
  except PageNotAnInteger:
    queryset = paginator.page(1)
  except EmptyPage:
    queryset = paginator.page(paginator.num_pages)
  context={
    "object_list":queryset,
    "page":"page",
    "username":username,
    "home":"blank",
    "home_views":"active",
    "profile":profile,
    "val":val,
    "percent":percent,
    "q":Question.objects.count(),
    "a":Answer.objects.count(),
    "u":User.objects.filter(Q(is_staff=False) | Q(is_superuser=False)).count(),
    "top":top
  }
  return render(request,"question/index.html",context)

@login_required(redirect_field_name='next', login_url=None)
def Question_delete(request,id,url):
  instance=get_object_or_404(Question,id=id,url=url)
  if request.user == instance.user:
    instance.user.questions = instance.user.questions-1
    instance.user.save()
    instance.delete()
    messages.success(request, "Successfully deleted")
  return HttpResponseRedirect('/')
