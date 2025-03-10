# from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password # for hashing pswrd
from django.contrib.auth.hashers import check_password
from datetime import timedelta
import datetime
from datetime import datetime, timedelta, date
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime, timedelta, date
from django.http import HttpResponse
from django.shortcuts import render

from django.conf import settings
import razorpay


import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import datetime
# from .models import Checkout, Payment  # Ensure your models are imported



# Create your views here.

def login_page_load(request):
    return render(request, 'login.html')

def doctor_signup_load(request):
    return render(request,'doctor_signup.html')

def doc_signup_post(request):
    docname = request.POST['name']
    docnumber = request.POST['phone']
    docemail = request.POST['email']
    docqualification = request.POST['qualification']
    docspecialisation = request.POST['specialisation']
    docgender = request.POST['gender']
    docusername = request.POST['username']
    docpassword = request.POST['password']
    docphoto = request.FILES['photo']
    
    if login_data.objects.filter(username=docusername).exists():
        return HttpResponse('''<script>alert("Username already taken! Please choose a different one.");window.location="/signup_page_load/"</script>''')

    
    doclogin=login_data()
    doclogin.username = docusername
    doclogin.password = docpassword
    doclogin.type='doctor'
    doclogin.save()
    
    doc_sign = doc_signup()
    doc_sign.docname = docname
    doc_sign.docnumber = docnumber
    doc_sign.docemail = docemail
    doc_sign.docqualification = docqualification
    doc_sign.docspecialisation = docspecialisation
    doc_sign.docgender = docgender
    doc_sign.docusername = docusername
    doc_sign.docpassword = docpassword
    doc_sign.docphoto = docphoto
    doc_sign.login=doclogin
    doc_sign.save()
    
    return HttpResponse('''<script>alert("Signup successfully");window.location="/login_page_load/"</script>''')
 

def login_data_post(request):
    username = request.POST['username']
    password = request.POST['password']
    user = login_data.objects.filter(username=username, password=password)
    if user.exists():
        user = login_data.objects.get(username=username, password=password)
        request.session['lid']=user.id
        
        # check the type of user
        if user.type == 'doctor': 
            return HttpResponse('''<script>alert("LogIn Successfully");window.location="/doctor_home_load/"</script>''')
        
        elif user.type == 'patient':
            return HttpResponse('''<script>alert("LogIn Successfully");window.location="/usr_home_load/"</script>''')
        else:
            return HttpResponse('''<script>alert("Unknone User Can't Login");window.location="//"</script>''')
    
    else:
        return HttpResponse('''<script>alert("LogIn Failed");window.location="//"</script>''')
 
def doctor_home_load(request):
    doctor = doc_signup.objects.get(login_id = request.session['lid'])
    return render(request, 'doctor_home.html',{'doctor':doctor})

def doc_profile(request):
    doc_db = doc_signup.objects.get(login_id = request.session['lid'])
    print(request.session['lid'])
    
    return render (request, 'doctor_profile.html', {'doc_profiles' :doc_db})

def doc_edit_profile_load(request):
    edit_doctor = doc_signup.objects.get(login_id=request.session['lid'])

    return render(request, 'doc_edit_profile.html',{'edit_doctor':edit_doctor})


def doc_edit_profile_post(request):
    edit_doctor = doc_signup.objects.get(login_id=request.session['lid'])
    print(request.session['lid'])

    # Update fields from form data 
    edit_doctor.docname = request.POST.get('name', edit_doctor.docname)
    edit_doctor.docnumber = request.POST.get('phone', edit_doctor.docnumber)
    edit_doctor.docemail = request.POST.get('email', edit_doctor.docemail)
    edit_doctor.docqualification = request.POST.get('qualification', edit_doctor.docqualification)
    edit_doctor.docspecialisation = request.POST.get('specialisation', edit_doctor.docspecialisation)
    edit_doctor.docgender = request.POST.get('gender', edit_doctor.docgender)
    edit_doctor.docusername = request.POST.get('username', edit_doctor.docusername)

    # Only update photo if a new one is uploaded
    if 'photo' in request.FILES:
        edit_doctor.docphoto = request.FILES['photo']

    # Save the updated details
    edit_doctor.save()
    
    return HttpResponse('''<script>alert("Edit Successfully");window.location="/doc_edit_profile_load/"</script>''')

def usr_signup_load(request):
    return render (request, 'user_signup.html')

def usr_signup_post(request):
    usr_name = request.POST['name']
    usr_phone = request.POST['phone']
    usr_mail = request.POST['email']
    usr_age = request.POST['age']
    usr_username = request.POST['username']
    usr_password = request.POST['password']
    usr_photo = request.FILES['photo']

    if login_data.objects.filter(username=usr_username).exists():
        return HttpResponse('''<script>alert("Username already taken! Please choose a different one.");window.location="/usr_signup_load/"</script>''')

    doclogin = login_data()
    doclogin.username = usr_username
    doclogin.password = usr_password
    doclogin.type = 'patient'
    doclogin.save()
    
    usr_signup_db = user_signup()
    usr_signup_db.usr_name = usr_name
    usr_signup_db.usr_number = usr_phone
    usr_signup_db.usr_mail = usr_mail
    usr_signup_db.usr_age = usr_age
    usr_signup_db.usr_username = usr_username
    usr_signup_db.user_password = usr_password
    usr_signup_db.user_photo = usr_photo
    usr_signup_db.login = doclogin  # Set the login field to the newly created login_data instance
    usr_signup_db.save()
    
    return HttpResponse('''<script>alert("SignUp Successfully");window.location="/login_page_load/"</script>''')

def usr_home_load(request):
    return render(request, 'user_home.html')

def usr_profile(request):
    usr_profile_db = user_signup.objects.get(login_id = request.session['lid'])
    print(request.session['lid'])
    
    return render (request, 'user_profile.html', {'usr_profile_db' :usr_profile_db})
# ****************************


def edit_user_profile_load(request):
    edit_usr_db = user_signup.objects.get(login_id = request.session['lid'])
    return render (request, 'usr_edit_profile.html', {'profile_edit':edit_usr_db})

def edit_user_profile_post(request):
    profile_edit = user_signup.objects.get(login_id=request.session['lid'])
    print(request.session['lid'])
    
# Update fields from form data 
    profile_edit.usr_name = request.POST.get('name', profile_edit.usr_name)
    profile_edit.usr_number = request.POST.get('phone', profile_edit.usr_number)
    profile_edit.usr_mail = request.POST.get('email', profile_edit.usr_mail)
    profile_edit.usr_age = request.POST.get('age', profile_edit.usr_age)
    profile_edit.usr_username = request.POST.get('username', profile_edit.usr_username)
    profile_edit.user_photo = request.POST.get('photo', profile_edit.user_photo)
    
# Only update photo if a new one is uploaded
    if 'photo' in request.FILES:
        profile_edit.user_photo = request.FILES['photo']
        
# save the updated details
    profile_edit.save()
    
    return HttpResponse('''<script>alert("Edit Successfully");window.location="/usr_profile/"</script>''')

def doctors_list_usr(request):
    doctors_list_tbl = doc_signup.objects.all()
    return render (request, 'list_doctors_user.html', {'data':doctors_list_tbl})


def add_patients_load(request):
    # user = user_signup.objects.get(request.session['lid']==id)
    return render (request, 'add_patients.html')

# def add_patients_post(request):
#     pname = request.POST['name']
#     page = request.POST['age']
#     pgender = request.POST['gender']
#     pdescription = request.POST['description']
#     #database table
#     tpatients = add_patients()
#     tpatients.Name = pname
#     tpatients.Age = page
#     tpatients.Gender = pgender
#     tpatients.Description = pdescription
#     tpatients.save()
#     return HttpResponse('''<script>alert("Submit Successfully");window.location="/usr_home_load/"</script>''')

def view_doctor_schedule(request):
    doctor = doc_signup.objects.get(login_id=request.session['lid'])
    doctortime = doctor_time.objects.filter(Drname_id=doctor)
    
    # Fetch the time slots for each schedule
    slots = []
    for schedule in doctortime:
        slot = Slots.objects.filter(schedule=schedule).first()
        if slot:
            slots.extend(slot.status.split(','))
    
    return render(request, 'doctor_schedule.html', {'doctortime': doctortime, 'slots': slots})

def add_schedule(request,id):
    schedule_id=doctor_time.objects.get(id=id)
    return render (request, 'add_schedule.html',{'data':schedule_id})



def add_schedule_post(request):
    if request.method == "POST":
        no_of_slots = request.POST.get('slots')
        slot_id = request.POST.get('slot_id')

        if not no_of_slots or not slot_id:
            return HttpResponse("Enter the number of slots and a valid slot ID", status=400)

        try:
            no_of_slots = int(no_of_slots)  # Convert to integer
            schedule = doctor_time.objects.get(id=slot_id)
        except ValueError:
            return HttpResponse("Invalid number of slots", status=400)
        except doctor_time.DoesNotExist:
            return HttpResponse("Invalid slot ID", status=404)

        start_time = schedule.Fromtime
        end_time = schedule.Totime

        # Calculate total available duration in minutes
        total_duration = (datetime.combine(date.today(), end_time) - 
                          datetime.combine(date.today(), start_time)).total_seconds() / 60
        
        if no_of_slots <= 0 or total_duration <= 0:
            return HttpResponse("Invalid slot count or time range", status=400)

        # Compute duration of each slot in minutes
        slot_duration = total_duration // no_of_slots  # Floor division to ensure even slots

        # Generate time slots sequentially
        time_slots = []
        current_time = start_time
        for _ in range(no_of_slots):
            time_slots.append(current_time.strftime('%I:%M %p'))
            current_time = (datetime.combine(date.today(), current_time) + timedelta(minutes=slot_duration)).time()

        # Store in the database
        slotsdb = Slots(
            schedule=schedule,
            NoOfSlots=no_of_slots,
            status=','.join(time_slots)  # Save as comma-separated times
        )
        slotsdb.save()

        return HttpResponse('''<script>alert("Slots added successfully");window.location="/view_doctor_schedule/"</script>''')


from datetime import datetime, timedelta
from django.shortcuts import render



def notification(request):
    messages = Notification.objects.all()
    return render (request, 'notification.html', {'messages':messages})

def notification_dr(request):
    messages = Notification.objects.all()
    return render (request, 'notification.html', {'messages':messages})




from django.shortcuts import render
from datetime import datetime, timedelta

# def view_time_slot(request, id):
#     # Fetch the doctor_time object
#     doctor_schedule = doctor_time.objects.get(id=id)

#     start_time = doctor_schedule.Fromtime
#     end_time = doctor_schedule.Totime

#     # Fetch or create the slot entry
#     slot_entry = Slots.objects.filter(schedule=doctor_schedule).first()

#     try:
#         no_of_slots = int(slot_entry.NoOfSlots) 
#     # if slot_entry and slot_entry.NoOfSlots else None
#     except ValueError:
#                    no_of_slots = None  # Handle invalid conversion

#     time_slots = []
#     if no_of_slots and no_of_slots > 0:
#         total_duration = (datetime.combine(datetime.today(), end_time) - 
#                           datetime.combine(datetime.today(), start_time))
#         slot_duration = total_duration / no_of_slots

#         current_time = start_time
#         for _ in range(no_of_slots):
#             next_time = (datetime.combine(datetime.today(), current_time) + slot_duration).time()

#             # Save the time slot period to the database
#             SlotPeriod.objects.get_or_create(
#                 # slot=slot_entry, 
#                 start_time=current_time, 
#                 end_time=next_time
#             )

#             # Store time periods for display
#             time_slots.append(f"{current_time.strftime('%I:%M %p')} - {next_time.strftime('%I:%M %p')}")

#             current_time = next_time  # Move to next time slot

#     return render(request, 'view_time_slot_dr.html', {
#         'doctor_schedule': doctor_schedule,
#         'no_of_slots': no_of_slots if no_of_slots else "N/A",
#         'time_slots': time_slots
#     })
 
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from .models import doctor_time, Slots, SlotPeriod

def view_time_slot(request, id):
    # Fetch the doctor_time object
    doctor_schedule = get_object_or_404(doctor_time, id=id)

    start_time = doctor_schedule.Fromtime
    end_time = doctor_schedule.Totime

    # Fetch or create the slot entry
    slot_entry = Slots.objects.filter(schedule=doctor_schedule).first()

    try:
        no_of_slots = int(slot_entry.NoOfSlots) if slot_entry and slot_entry.NoOfSlots else None
    except ValueError:
        no_of_slots = None  # Handle invalid conversion

    time_slots = []
    if no_of_slots and no_of_slots > 0:
        total_duration = (datetime.combine(datetime.today(), end_time) - 
                          datetime.combine(datetime.today(), start_time))
        slot_duration = total_duration / no_of_slots

        current_time = start_time
        for _ in range(no_of_slots):
            next_time = (datetime.combine(datetime.today(), current_time) + slot_duration).time()

            # Save the time slot period to the database
            SlotPeriod.objects.get_or_create(
                doctor=doctor_schedule.Drname,  # Correct field
                schedule=doctor_schedule,  # Add schedule reference
                start_time=current_time, 
                end_time=next_time
            )

            # Store time periods for display
            time_slots.append(f"{current_time.strftime('%I:%M %p')} - {next_time.strftime('%I:%M %p')}")

            current_time = next_time  # Move to next time slot

    return render(request, 'view_time_slot_dr.html', {
        'doctor_schedule': doctor_schedule,
        'no_of_slots': no_of_slots if no_of_slots else "N/A",
        'time_slots': time_slots
    })

def user_view_slot(request, id):
    # Fetch doctor_time objects based on Drname_id
    user_slot = doctor_time.objects.filter(Drname_id=id)
    print(user_slot)
    slots_data = []
    for slot in user_slot:
        start_time = slot.Fromtime
        end_time = slot.Totime
        
        # Fetch SlotPeriod entries linked to this doctor
        slot_periods = SlotPeriod.objects.filter(doctor_id=id).values('id', 'start_time', 'end_time')
        
        slots_data.append({
            'date': slot.Date,
            'from_time': slot.Fromtime.strftime('%I:%M %p'),
            'to_time': slot.Totime.strftime('%I:%M %p'),
            'no_of_slots': len(slot_periods),
            'slot_periods': slot_periods,  # Pass SlotPeriod objects
        })

    return render(request, 'doctors_sloat_usr.html', {'slots_data': slots_data})

    
def feedback(request, id):
    doc = get_object_or_404(doc_signup, id=id)  # Safer way to fetch object
    return render(request, 'feedback.html', {'doc': doc})

def feedback_post(request):
    subject = request.POST['subject']
    message = request.POST['message']
    doctor_id=request.POST.get('id')
    doctor = doc_signup.objects.get(id=doctor_id)
    Feedback_model = feedback_model()
    Feedback_model.subject = subject
    Feedback_model.message = message
    Feedback_model.Drname = doctor
    Feedback_model.save()
    return HttpResponse('''<script>alert("Submit Successfully");window.location="/doctors_list_usr/"</script>''')

def view_feedback(request,id):
    # Fetch all feedback entries from the database
    feedback_list = feedback_model.objects.filter(Drname=id)    #filtering 
    
    # Pass the feedback list to the template
    return render(request, "view_feedback.html", {'feedback_list': feedback_list})

from django.shortcuts import redirect, HttpResponse
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from .models import SlotPeriod, Booking, user_signup  # Ensure models are imported

def book_doctor(request):
    if request.method == 'POST':
        selected_time_id = request.POST.get('selected_time')
        pname = request.POST.get('name')
        page = request.POST.get('age')
        pgender = request.POST.get('gender')
        pdescription = request.POST.get('description')

        if not selected_time_id:
            return HttpResponse(
                '''<script>alert("Please select a time slot.");window.location="/schedule_appointment/"</script>'''
            )

        # Fetch the SlotPeriod instance
        try:
            slot_period = SlotPeriod.objects.get(id=selected_time_id)
        except SlotPeriod.DoesNotExist:
            return HttpResponse(
                '''<script>alert("Invalid time slot selected.");window.location="/schedule_appointment/"</script>'''
            )

        # Fetch the logged-in user
        try:
            users = user_signup.objects.get(login_id=request.session.get('lid'))
        except user_signup.DoesNotExist:
            return HttpResponse(
                '''<script>alert("User not found. Please log in again.");window.location="/login/"</script>'''
            )

        # Ensure the slot has an associated doctor
        if not slot_period.doctor:
            return HttpResponse(
                '''<script>alert("This time slot is not linked to a doctor. Contact support.");window.location="/schedule_appointment/"</script>'''
            )

        # Check if the slot is already booked
        if slot_period.is_booked:
            return HttpResponse(
                '''<script>alert("This time slot is already booked. Choose another.");window.location="/schedule_appointment/"</script>'''
            )

        # Save booking entry in Booking table
        booking_entry = Booking.objects.create(
            slot_period=slot_period,  # Save SlotPeriod, not Slots
            doctor=slot_period.doctor,  # Ensure doctor_id is included
            users=users,
            status="Pending",
            date=datetime.today(),
            Name=pname,
            Age=page,
            Gender=pgender,
            Description=pdescription
        )

        # Mark the slot as booked
        slot_period.is_booked = True
        slot_period.save()

        return HttpResponse(
            '''<script>alert("Booking Successful!");window.location="/view_booking_user/"</script>'''
        )

    return redirect('/schedule_appointment/')


# def prescriptionLoad(request,id):
#     # petientName = add_patients.objects.get(id=id)
    
#     return render (request, 'prescription.html', {'patient':petientName})

def view_patients(request):
    appointments = Booking.objects.filter(slot_period__schedule__Drname__login_id=request.session['lid'])
    return render(request, 'view_patients.html', {'patients': appointments})

def prescripton_page_load(request, id):
    details = Booking.objects.get(id=id)
    return render (request, 'send_prescription.html', {'patient' : details})

def post_prescription(request):
    print("Request received!")  # Debugging statement
    id = request.POST['id']
    Symptoms = request.POST['symptoms']
    Diagnosis = request.POST['diagnosis']
    Prescribed_Med = request.POST['medications']
    print(id)
    medical_note = medical_notes()
    medical_note.symptoms = Symptoms
    medical_note.diagnosis = Diagnosis
    medical_note.priscription = Prescribed_Med
    medical_note.patients = Booking.objects.get(id=id)
    medical_note.doctors = doc_signup.objects.get(login_id=request.session['lid'])
    medical_note.save()
    return HttpResponse('''<script>alert("Send Successful!");window.location="/view_patients/"</script>''')
    


# def view_prescription_doctor(request, id):
#     doctor = medical_notes.objects.get(patients_id=id)
#     return render(request, 'view_prescription_doctor.html', {'prescription':doctor})
def view_prescription_doctor(request, id):
    prescriptions = medical_notes.objects.filter(patients_id=id)  
    return render(request, 'view_prescription_doctor.html', {'prescriptions': prescriptions})




def view_prescription_user(request):
    prescriptions = medical_notes.objects.filter(patients__users__login_id=request.session['lid'])  
    return render(request, 'view_prescription_user.html', {'prescriptions': prescriptions})
    


# def view_booking_user(request):
#     booking = Booking()
#     booking.users = user_signup.objects.get(login_id = request.session['lid'])
#     return render (request, 'view_booking.html', {'booking': booking})
from django.shortcuts import render
from .models import Booking, user_signup

def view_booking_user(request):
    # Get the logged-in user's ID from the session
    user_id = request.session.get('lid')
    
    # Filter bookings based on the logged-in user
    bookings = Booking.objects.filter(users__login_id=user_id)
    # bookings = Booking.objects.filter(users__login_id=user_id)
    
    # Pass the filtered bookings to the template
    return render(request, 'view_booking.html', {'bookings': bookings})


razorpay_api_key = settings.RAZORPAY_API_KEY
razorpay_secret_key = settings.RAZORPAY_API_SECRET
razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

@csrf_exempt
def paymentt(request,id):
    booking= get_object_or_404(Booking, id=id)
    # Amount to be paid (in paisa), you can change this dynamically based on your logic
    amount = 500
    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1', # Auto-capture payment
    }
    # Create an order
    order = razorpay_client.order.create(data=order_data)
    print(order)
    callback_url = 'paymenthandler/'
    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': amount,
        'currency': order_data['currency'],
        # 'order_id': order['id'],
        'b_id':booking.id,
        'callback_url':callback_url
    }
    return render(request, 'payment.html', context)

def payment_post(request):
    amount = int(request.POST['amount']) / 100  # Convert it back

    b_id = request.POST['b_id']
    print(b_id)
    tpayment = payment(
        amount=amount,
        booking_id=b_id,
        date = datetime.now()
    )
    cc=Booking.objects.get(id=b_id)
    cc.status= 'Completed'
    cc.save()
    tpayment.save()


    return HttpResponse('''<script>alert("Payment successfull! Thanks for Shopping with us!");window.location="/orders_history/"</script>''')