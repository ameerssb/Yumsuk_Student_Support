from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect,get_object_or_404
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from verify_email.email_handler import send_verification_email
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from question.models import Question, Answer
from .forms import VerifyForm, Update, CreateUserForm
from .models import User
from .decorators import user_sigin
from . import verify



signout_deco = [login_required]
sigin_reg_deco = [user_sigin(User,'home')]

class Home(View):
    def get(self,request):
        context = {}

        return render(request, 'account/index.html', context)

    def post(self,request):
        return render(request, 'account/index.html')

@method_decorator(sigin_reg_deco, name='get')
@method_decorator(sigin_reg_deco, name='post')
#@method_decorator(ver)
class Signin(View):
    def get(self,request):

        context = {}

        return render(request, 'account/signin.html', context)

    def post(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            if request.POST['email'] and request.POST['password']:
                email = request.POST['email']
                password = request.POST['password']
                user = authenticate(email=email, password=password)
                u = User.objects.filter(email=email).first()
                if user is not None:
                    if user.is_active:
                        if u.is_email_verified:
                          login(request, user)
                          if request.GET.get('next'):
                              return redirect(request.GET.get('next'))
                          else:  
                              return redirect('home')
                        else:
                          messages.error(request,"Your email is not verified, Please verify before Signing in")
                          return redirect('Signin')                    
                    else:
                        messages.error(request,"Your account is disabled, Contact Us via Suppport Team")
                        return redirect('Signin')                    
                else:
                    messages.error(request, "Invalid username or password")
                    return redirect('Signin')
            else:
                messages.error(request,"Error while Submitting request please check form and re-submit")
                return redirect('Sigin')

@method_decorator(signout_deco, name='get')
class Signout(View):
    def get(self,request):
        logout(request)
        return redirect('Signin')

@method_decorator(sigin_reg_deco, name='get')
@method_decorator(sigin_reg_deco, name='post')
class Register(View):
    def get(self,request):
        
        form = CreateUserForm()
#        print(form)
        context = {'form':form,}

        return render(request, 'account/register.html', context)

    def post(self,request):

        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                send_verification_email(request, form)
                messages.success(request, "Account created. check your email inbox to verify your account")
                return redirect('Signin')
            except:
                messages.error(request, "an error occured while sending verification to your email, can't create your account at this time")
                return redirect('Register')
        else:
                messages.error(request, "Registration form is not filled correctly")
                return redirect('Register')

@method_decorator(sigin_reg_deco, name='get')
@method_decorator(sigin_reg_deco, name='post')
class password_reset_request(View):
    def get(self,request):
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="account/password_reset.html", context={"password_reset_form":password_reset_form})        

    def post(self,request):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "account/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Yumsuk Journals',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'noreply<support@yumsukjournals.com>' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    except:
                        messages.error(request,'an error occured while trying to send password reset details, Check your internet connection or try again later')
                        return redirect('Signin')
                    return redirect ("/accounts/password_reset/done/")
    
@login_required(redirect_field_name='next', login_url=None)
def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            if not request.user.is_verified:
                code = form.cleaned_data.get('code')
                if verify.check(request.user.phone, code):
                    request.user.is_verified = True
                    request.user.save()
                    return redirect('home')
                else:
                    messages.error(request, "incorrect verification code")
                    redirect('verify')
            else:
                redirect('home')
    else:
        form = VerifyForm()
    return render(request, 'core/verify.html', {'form': form})

@login_required
def reverify_code(request):
    phone = request.user.phone
    verify.send(str(phone))
    return redirect('verify')

@login_required
def profile(request, username):
  top = User.objects.filter(Q(is_staff=False) | Q(is_superuser=False)).order_by("-points")[:min(User.objects.count(),5)]
  if request.user.is_authenticated:
    id = User.objects.get(username=username)
    profile = get_object_or_404(User,id=id.id)
    if profile.points < 100:
      color = "#3498db"
      rank = "Amateur"
    elif profile.points < 1000:
      color = "#1abc9c"
      rank = "Trainee"
    elif profile.points < 2000:
      color = "gold"
      rank = "Professor"
    else:
      color = "red"
      rank = "Legend"
  else:
    profile = get_object_or_404(User,id=1)
    val = ""
    percent = 100

  queryset_list=Question.objects.all().filter(user=profile).order_by("-created")
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


  queryset_list1=Answer.objects.all().filter(user=profile).order_by("-created")
  paginator1 = Paginator(queryset_list1, 10)
  page1 = request.GET.get('page1')
  username='Login'
  if User.is_active:
    username = User.username
  try:
    queryset1 = paginator1.page(page1)
  except PageNotAnInteger:
    queryset1 = paginator1.page(1)
  except EmptyPage:
    queryset1 = paginator1.page(paginator1.num_pages)


  context={
    "profile":profile,
    "color":color,
    "rank": rank,
    "object_list":queryset,
    "page":"page",
    "object_list1":queryset1,
    "page1":"page1",
    "q":Question.objects.count(),
    "a":Answer.objects.count(),
    "u":User.objects.filter(Q(is_staff=False) | Q(is_superuser=False)).count(),
    "top":top
  }
  return render(request,"profile.html",context)

@login_required
def Update_pro(request, username):
  top = User.objects.filter(Q(is_staff=False) | Q(is_superuser=False)).order_by("-points")[:min(User.objects.count(),5)]
  id = User.objects.get(username=username)
  profile = get_object_or_404(User,id=id.id)
  instance=get_object_or_404(User,id=id.id)
  if request.user.username == instance.username:
    form = Update(request.POST or None, request.FILES or None,instance=instance)
    if form.is_valid():
      instance=form.save(commit=False)
      instance.save()
      messages.success(request, "Saved")
      return HttpResponseRedirect('/')
    context={
      "instance":instance,
      "form":form,"q":Question.objects.count(),"a":Answer.objects.count(),"u":User.objects.count(),"top":top,
      "profile":profile
    }
    return render(request,"update.html",context)
  else:
    messages.error(request, "User unauthorized.")
    return HttpResponseRedirect('/')

@login_required
def User_list(request):
  top = User.objects.filter(Q(is_staff=False) | Q(is_superuser=False)).order_by("-points")[:min(User.objects.count(),5)]
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


  queryset_list=User.objects.filter(Q(is_staff=False) | Q(is_superuser=False)).order_by("username")
  query=request.GET.get('q')
  if query:
    queryset_list=queryset_list.filter(
    Q(location__icontains=query)|
    Q(user__username__icontains=query)
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
    "profile":profile,
    "val":val,
    "percent":percent,
    "q":Question.objects.count(),
    "a":Answer.objects.count(),
    "u":User.objects.filter(Q(is_staff=False) | Q(is_superuser=False)).count(),
    "top":top
  }
  return render(request,"user.html",context)
