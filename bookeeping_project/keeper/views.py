from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from keeper.forms import UserForm, UserProfileForm, ProjectForm, ContractorForm
from keeper.models import Project, Contractor

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from datetime import datetime




def user_login(request):
	context_dict={}
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		
		user=authenticate(username=username, password=password)
		

		if user:

			if user.is_active:
				login(request, user)
				return HttpResponseRedirect("/keeper/dashboard")
			else:
				return HttpResponse("Your account is disabled")
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid Login details supplied")
	else:
		return render(request, 'keeper/index.html', {})



@login_required
def restricted(request):
	return HttpResponse("")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect("/keeper/")





def addContractor(request):
	context_dict={}
	registered=False
	if request.method=="POST":
		contractor_form=ContractorForm(data=request.POST)

		if contractor_form.is_valid():
			contractor=contractor_form.save()
			registered=True

		else:
			print contractor_form.errors
	else:
		contractor_form=ContractorForm()

	return render(request, 'keeper/addContractor.html', {'contractor_form':contractor_form, 'registered':registered})








def dashboard(request):
	
	context_dict={}

	
	project_list=Project.objects.filter(client__user=request.user).order_by('-title')
	print project_list
	contractor_list=Contractor.objects.order_by('-name')

	context_dict['Projects']=project_list
	context_dict['Contractors']=contractor_list

	return render(request, 'keeper/dashboard.html', context_dict)



def addProject(request):
	context_dict={}
	current_user=None
	if request.user.is_authenticated():
		current_user=request.user.username
		context_dict['user_name']=current_user
		print current_user
		contractor_list=Contractor.objects.all()
		context_dict['contractor_list']=contractor_list
		
		if request.method=="POST":
			form=ProjectForm(request.POST)
			project_title=request.POST.get('title')
			contractor_value=request.POST.get('contractor_selected')
			contractor=Contractor.objects.get(name=contractor_value)
			print project_title, contractor
			if form.is_valid():
				form.save(commit=True)
				get_recent_project=Project.objects.get(title=project_title)
				print get_recent_project
				get_clientOfProject=get_recent_project.client
				get_clientOfProject=current_user
				get_recent_project.save()
				get_recent_project.contractor.add(contractor)
				print get_recent_project.contractor.all()
				print get_clientOfProject
				return success(request)
			else:
				print form.errors
		else:
			form=ProjectForm()
			context_dict['form']=form
	else:
		print "none"
	return render(request, 'keeper/addProject.html', context_dict)


def update_contractor(request, project_slug):
	context_dict={}
	contractor_list=Contractor.objects.all()
	context_dict['contractors']=contractor_list
	project_to_be_updated=Project.objects.get(slug=project_slug)
	context_dict['current_project']=project_to_be_updated
	print project_to_be_updated.title
	if request.method=="POST":
		project_tobeUpdated=Project.objects.get(slug=project_slug)
		print project_tobeUpdated.title
		contractor_value=request.POST.get('contractor_selected')
		contractor=Contractor.objects.get(name=contractor_value)
		print contractor
		project_tobeUpdated.contractor.add(contractor)
		print project_tobeUpdated.contractor.all()
		return HttpResponseRedirect("/keeper/dashboard ")
	else:
		print "NONE"

	return render(request, 'keeper/update_contractor.html', context_dict)

def success(request):
	context_dict={}
	if request.method=="POST":
		form=ProjectForm(request.POST)
		context_dict['title']=form.__dict__["fields"]["title"]
	else:
		print"NONE"
	return render(request, 'keeper/success.html', context_dict)


def project_details(request, project_name_slug):
	context_dict={}

	try:
		project_selected=Project.objects.get(slug=project_name_slug)
		project_hours=project_selected.contractor_hours
	except Project.DoesNotExist:
		project_selected=None		

	project_revenue=0
	project_cost=10*project_hours
	#print project_selected.title, project_selected.contractor.all()		
	project_selected_contractors=project_selected.contractor.all()
	for i in project_selected_contractors:
		billRate=i.bill_rate
		project_revenue=project_revenue+(billRate*project_hours)

	context_dict['project_details']=project_selected
	context_dict['projectRevenue']=project_revenue
	context_dict['projectCost']=project_cost
	context_dict['project_contractors']=project_selected.contractor.all()

	return render(request, 'keeper/project_detail.html', context_dict)







def contractor_details(request, contractor_name_slug):
	context_dict={}
	
	try:
		contractor_selected=Contractor.objects.get(slug=contractor_name_slug)
		context_dict['contractor']=contractor_selected
		contractor_projects=contractor_selected.project_set.all()
	except Contractor.DoesNotExist:
		contractor_selected=None

	#print contractor_selected.name, contractor_selected.url, contractor_selected.bill_rate, contractor_projects


	return render(request, 'keeper/contractor_details.html', context_dict)





def register(request):

	registered = False
	if request.method=='POST':
		user_form=UserForm(data=request.POST)
		profile_form=UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user=user_form.save()
			user.set_password(user.password)
			user.save()

			profile=profile_form.save(commit=False)
			profile.user=user

			profile.save()
			registered=True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form=UserForm()
		profile_form=UserProfileForm()

	return render(request, 'keeper/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})