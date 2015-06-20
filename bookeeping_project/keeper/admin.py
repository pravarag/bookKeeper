from django.contrib import admin

# Register your models here.
from keeper.models import UserProfile, Project, Contractor

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Contractor)
