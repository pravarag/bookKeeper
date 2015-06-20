from django import forms

from keeper.models import UserProfile, Project, Contractor

from django.contrib.auth.models import User



class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model=User
		fields=('username', 'password')


class UserProfileForm(forms.ModelForm):
	class Meta:
		model=UserProfile
		fields=()



class ProjectForm(forms.ModelForm):

	title=forms.CharField(max_length=128, help_text="Enter Project Title: ")
	contractor_hours=forms.IntegerField(initial=0, help_text="Enter hours you want to hire contractor for: ")
	slug=forms.CharField(widget=forms.HiddenInput(), required=False)
	class Meta:
		model=Project
		fields=('title','contractor_hours',)





class ContractorForm(forms.ModelForm):

	name=forms.CharField(max_length=128, help_text="Please enter your name or your firm's name: ")
	bill_rate=forms.IntegerField(initial=0, help_text="Please enter your Bill rate")
	url=forms.CharField(max_length=128, help_text="Please enter your web-details: ")
	slug=forms.CharField(widget=forms.HiddenInput(), required=False)
	class Meta:
		model=Contractor
		fields=('name','bill_rate','url',)