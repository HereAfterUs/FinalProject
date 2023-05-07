from django.contrib import admin
from myApp.models import JobInfo, User, History


class JobManager(admin.ModelAdmin):
    list_display = ["id", "title", "address", "type", "educational", "workExperience", "workTag", "salary",
                    "salaryMonth",
                    "companyTags", "hrWork", "hrName", "practice", "companyTitle", "companyAvatar", "companyNature",
                    "companyStatus", "companyPeople", "detailUrl", "companyUrl", "dist"]

    list_display_links = ['title']
    list_editable = ["address", "type", "educational", "workExperience", "workTag", "salary", "salaryMonth",
                     "companyTags", "hrWork", "hrName", "practice", "companyTitle", "companyAvatar", "companyNature",
                     "companyStatus", "companyPeople", "detailUrl", "companyUrl", "dist"]
    list_filter = ['type']
    search_fields = ['title']
    readonly_fields = ['id']
    list_per_page = 20


class UserManager(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'avatar', 'createTime', 'address', 'educational', 'work', 'workExpirence']
    list_display_links = ['username']
    search_fields = ['username']
    list_editable = ['password', 'avatar', 'address', 'educational', 'work', 'workExpirence']
    readonly_fields = ['id']
    date_hierarchy = "createTime"



admin.site.register(JobInfo, JobManager)
admin.site.register(User, UserManager)

