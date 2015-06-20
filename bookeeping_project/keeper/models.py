
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class UserProfile(models.Model):	## the client is the user
	user=models.OneToOneField(User)

	def __unicode__(self):
		return self.user.username





class Contractor(models.Model):
	name=models.CharField(max_length=128)
	url=models.URLField()
	bill_rate=models.IntegerField(default=0)
	slug=models.SlugField(unique=True)
	
	def save(self, *args, **kwargs):
		self.slug=slugify(self.name)
		super(Contractor, self).save(*args, **kwargs)


	def __unicode__(self):
		return self.name



class Project(models.Model):
	contractor=models.ManyToManyField(Contractor)
	client=models.ForeignKey(UserProfile, null=True)
	title=models.CharField(max_length=128)
	slug=models.SlugField(unique=True)
	contractor_hours=models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		self.slug=slugify(self.title)
		super(Project, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title



