from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
def upload_location(instance, filename):
	return "%s/%s" %(instance.username, filename)


class User(AbstractUser):
	first_name = models.CharField(blank=False,null=False, max_length=50)
	last_name = models.CharField(blank=False,null=False, max_length=50)
	other_name = models.CharField(blank=True,null=False, max_length=50)
	email = models.EmailField(unique=True)
	is_active = models.BooleanField(default=True)
	Verified = models.BooleanField(default=True)
	is_email_verified = models.BooleanField(default=False)
	username = models.CharField(unique=False,max_length=30,blank=True)
	phone = models.CharField(max_length=14, null=True, blank=True)	
	image=models.ImageField(upload_to=upload_location, null=True)
	bio = models.TextField(blank=True,null=True)
	points=models.IntegerField(default=0)
	questions=models.IntegerField(default=0)
	answers=models.IntegerField(default=0)
	is_email_verified = models.BooleanField(default=False)
	is_phone_verified = models.BooleanField(default=False)
	date_of_birth = models.DateField(null=True, blank=True)

	class Gender(models.TextChoices):
		SELECT = 'SELECT'
		MALE = 'MALE'
		FEMALE = 'FEMALE'
		UNSPECIFIED = 'PREFERRED NOT TO SAY'
	gender = models.CharField(choices=Gender.choices, default="Select", max_length=20)
	created = models.DateTimeField(auto_now_add=True,auto_created=True)
	updated = models.DateTimeField(auto_now=True,auto_created=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name','last_name','username']

	def __str__(self):
		return self.username

