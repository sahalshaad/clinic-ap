from django.db import models
from datetime import date

# Create your models here.

class login_data(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "Login"
        verbose_name_plural = "Logins"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username}"
    
class doc_signup(models.Model):
    docname = models.CharField(max_length=100)
    docnumber = models.CharField(max_length=100)
    docemail = models.CharField(max_length=100)
    docqualification = models.CharField(max_length=50)
    docspecialisation = models.CharField(max_length=50)
    docgender = models.CharField(max_length=50, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    docusername = models.CharField(max_length=50)
    docpassword = models.CharField(max_length=50)
    docphoto = models.FileField(upload_to='photos/', null=True, blank=True) 
    login = models.ForeignKey(login_data, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.docname}"
    
class user_signup(models.Model):
    usr_name = models.CharField(max_length=100)
    usr_number = models.CharField(max_length=100)
    usr_mail = models.CharField(max_length=100)
    usr_age = models.CharField(max_length=100)
    usr_username = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)
    user_photo = models.FileField(upload_to='photos/', null=True, blank=True)
    login = models.ForeignKey(login_data, on_delete=models.CASCADE)
    
  
class doctor_time(models.Model):
    Drname = models.ForeignKey(doc_signup, on_delete=models.CASCADE)
    Date = models.DateField()
    Fromtime = models.TimeField()
    Totime = models.TimeField()
    
class Slots(models.Model):
    schedule = models.ForeignKey(doctor_time, on_delete=models.CASCADE)
    NoOfSlots = models.CharField(max_length=100)
    status = models.TextField(default = 'Free')
    booked_slots = models.TextField(default='')  # Stores booked slots as comma-separated values

class Notification(models.Model):
    message = models.TextField()
    date = models.DateTimeField()

class feedback_model(models.Model):
    Drname = models.ForeignKey(doc_signup, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    
    def __str__(self):
        return f"{self.subject}"
    

    

    
class SlotPeriod(models.Model):
    doctor = models.ForeignKey(doc_signup, on_delete=models.CASCADE)  # Ensure this exists
    schedule = models.ForeignKey(doctor_time, on_delete=models.CASCADE)  # Add schedule reference
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor.docname} ({self.start_time} - {self.end_time})"

    
class Booking(models.Model):
    slot_period = models.ForeignKey(SlotPeriod, on_delete=models.CASCADE)
    doctor = models.ForeignKey(doc_signup, on_delete=models.CASCADE)  # Add doctor reference
    users = models.ForeignKey(user_signup, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="Pending")
    date = models.DateField()
    Name = models.CharField(max_length=100)
    Age = models.IntegerField()
    Gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    Description = models.TextField()

    def __str__(self):
        return f"Booking for {self.Name} with Dr. {self.doctor.docname}"

        
class medical_notes(models.Model):    
    patients = models.ForeignKey(Booking, on_delete=models.CASCADE)
    doctors = models.ForeignKey(doc_signup, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    priscription = models.CharField(max_length=200)
    symptoms = models.CharField(max_length=100)
    diagnosis = models.CharField(max_length=100)
    
class payment(models.Model):
    amount = models.CharField(max_length=100)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    date = models.DateField()
    
    