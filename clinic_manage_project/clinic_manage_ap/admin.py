from django.contrib import admin
from .models import *

# Register your models here.
class logadmin(admin.ModelAdmin):
    list_display=["username", "password", "type"]
    readonly_fields = ["password"]
    
admin.site.register(login_data, logadmin)

class user_signup_admin(admin.ModelAdmin):
    list_display=["usr_name", "usr_number", "usr_mail", "usr_age", "usr_username", "user_photo"]
    readonly_fields=["user_password"]
    
admin.site.register(user_signup, user_signup_admin)

class doctor_signup_admin(admin.ModelAdmin):
    list_display=["docname", "docnumber", "docemail", "docqualification", "docspecialisation", "docgender", "docusername", "docphoto"]
    readonly_fields=["docpassword"]
admin.site.register(doc_signup, doctor_signup_admin)

# class add_patients_admin(admin.ModelAdmin):
#     list_display = ["Name", "Age", "Gender"]
#     readonly_fields = ["Description"]
# admin.site.register(add_patients, add_patients_admin)

class doctor_time_admin(admin.ModelAdmin):
    list_display = ["Drname", "Date", "Fromtime", "Totime"]
admin.site.register(doctor_time, doctor_time_admin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ["message", "date"]
admin.site.register(Notification, NotificationAdmin)
    
class feedbackadmin(admin.ModelAdmin):
    readonly_fields = ["Drname", "subject", "message"]
admin.site.register(feedback_model, feedbackadmin)