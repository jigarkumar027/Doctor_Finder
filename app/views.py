from django.shortcuts import render,HttpResponseRedirect,reverse,redirect
from .models import *
from random import randint
from .utils import *
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
import socket
socket.getaddrinfo('localhost',8080)
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def pharmacy(request):
    return render(request,'app/pricing.html')

def Indexpage(request):
    return render(request,"app/index.html")

def DoctorDetails(request):
    return render(request,"app/doctors-details.html")

def ContactPage(request):
    return render(request,"app/contact.html")

def AboutusPage(request):
    return render(request,"app/about.html")

def Blog(request):
    return render(request,"app/blog.html")

def How_It_Works(request):
    return render(request,"app/how_it_works.html")

def FAQ(request):
    return render(request,"app/FAQ.html")

def PatientDash(request):
    udata = User.objects.get(id=request.session['id'])
    patient_id = Patient.objects.get(user_id=udata)
    print('****@@@')
    print(patient_id.id)
    print('^^^^^')
    allDoc = Doctor.objects.all()
    totaldoc = len(allDoc)
    print(totaldoc)
    allpat = Patient.objects.all()
    totalpat = len(allpat)
    print(totalpat)
    all_appo = Appointment.objects.filter(patient_id=patient_id.id,appointment_status=True)
    totalappo = len(all_appo)
    print('*********************')
    print(totalappo)
    return render(request,"app/patient-dashboard.html",{'key60':all_appo,'doccount':totaldoc,'patcount': totalpat, 'appocount' : totalappo})

def DoctorDash(request):
    udata = User.objects.get(id=request.session['id'])
    doctor_id = Doctor.objects.get(user_id=udata)
    allpat = Patient.objects.all().filter()
    totalpat = len(allpat)
    print(totalpat)
    allDoc = Doctor.objects.all()
    totaldoc = len(allDoc)
    print(totaldoc)
    all_appo = Appointment.objects.all().filter(doctor_id=doctor_id,appointment_status = False)
    totalappo = len(all_appo)
    print(totalappo)
    return render(request,"app/doctors-dashboard.html",{'key61':all_appo,'patcount': totalpat,'doccount':totaldoc, 'appocount' : totalappo})

def PharmacyDash(request):
    return render(request,"app/admin/pharmacy-dashboard.html")

def TermsAndConditionsPage(request):
    return render(request,"app/Terms-conditions.html")

def Privacy_Policy(request):
    return render(request,"app/privacy_policy.html")


# ============= Register pages ===============

def DoctorRegisterPage(request):
    return render(request,"app/doctorregister.html")

def PharmacyRegisterPage(request):
    return render(request,"app/pharmaregister.html")

def PaitentRegisterPage(request):
    return render(request,"app/paitentregister.html")

def InsertData(request):
    try:
        if request.POST['role']=="Doctor":
            role = request.POST['role']
            fname = request.POST['fname']   
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['pass']
            cpassword = request.POST['cpass']
            print('****************************')
            user = User.objects.filter(Email=email)
            if user:
                message = "Email already exits"
                return render(request,"app/doctorregister.html",{'msg':message})
            else:
                if password==cpassword:
                    otp = randint(10000,99999)
                    newuser = User.objects.create(Email=email,Password=password,Role=role,Otp=otp)
                    newdoc = Doctor.objects.create(user_id=newuser,Firstname=fname,Lastname=lname)
                    email_subject = "Doctor Varification"
                    print('###########*-*********')
                    sendmaildoc(email_subject, 'Email', email, {'name': fname ,'otp': otp})
                    return render(request,"app/otpverify.html",{'key55':newuser})
                else:
                    message = "password and conform password does not match"
                    return render(request,"app/doctorregister.html",{'msg':message})

        elif request.POST['role']=="Patient":
                    role = request.POST['role']
                    fname = request.POST['fname']   
                    lname = request.POST['lname']
                    email = request.POST['email']
                    password = request.POST['pass']
                    cpassword = request.POST['cpass']

                    user = User.objects.filter(Email=email)
                    if user:
                        message = "Email already exits"
                        return render(request,"app/paitentregister.html",{'msg':message})
                    else:
                        if password==cpassword:
                            otp = randint(10000,99999)
                            newuser = User.objects.create(Email=email,Password=password,Role=role,Otp=otp)
                            newpat = Patient.objects.create(user_id=newuser,Firstname=fname,Lastname=lname)
                            email_subject = "Patient Varification"
                            sendmailpat(email_subject, 'Email', email, {'name': fname ,'otp': otp})
                            return render(request,"app/otpverify.html",{'key55':newuser})
                        else:
                 
                            message = "password and conform password does not match"
                            return render(request,"app/paitentregister.html",{'msg':message}) 
        else: 
                if request.POST['role']=="Pharmacy":
                    role = request.POST['role']
                    fname = request.POST['fname']   
                    pname = request.POST['pname']
                    email = request.POST['email']
                    password = request.POST['pass']
                    cpassword = request.POST['cpass']

                    user = User.objects.filter(Email=email)
                    if user:
                        message = "Email already exits"
                        return render(request,"app/pharmaregister.html",{'msg':message})
                    else:
                        if password==cpassword:
                            otp = randint(10000,99999)
                            newuser = User.objects.create(Email=email,Password=password,Role=role,Otp=otp)
                            newpat = Pharmacy.objects.create(user_id=newuser,FullName=fname,PharmaName=pname)
                            email_subject = "Pharmacy Varification"
                            sendmailpha(email_subject, 'Email', email, {'name': fname ,'otp': otp})
                            return render(request,"app/otpverify.html",{'key55':newuser})
                        else:
                            message = "password and conform password does not match"
                            return render(request,"app/pharmaregister.html",{'msg':message})              
    except Exception as e:
        print("Regitration exception ------------>",e)

# ==============  Login Pages Views =================

def DoctorLoginpage(request):
    return render(request,"app/doctor-login.html")

def PatientLoginpage(request):
    return render(request,"app/patient-login.html")

def PharmacyLoginpage(request):
    return render(request,"app/pharmacy-login.html")

def VerifyOtp(request):
    print("------------1--------------")
    try:
        email=request.POST['email']
        eotp=request.POST['eotp']
        print("Eotp--------------->",eotp)
        print(type(eotp))
        user = User.objects.get(Email=email)
        if user.Otp==eotp and user.Role =="Doctor":
            print("===========2=========")
            message = "otp verified successfully"
            return render(request,"app/doctor-login.html",{'msg':message})
        elif user.Otp==eotp and user.Role =="Patient":
            message = "otp verified successfully"
            return render(request,"app/patient-login.html",{'msg':message})
        else:
            if user.Otp==eotp and user.Role =="Pharmacy":
                message = "otp verified successfully"
                return render(request,"app/pharmacy-login.html",{'msg':message})
    except Exception as e:
        print("OTP Verify Exception-------------->",e)


def Loginuser(request):
    try:
        if request.POST['role']=="Doctor":
            email = request.POST['email']
            password = request.POST['pass']

            user = User.objects.get(Email=email)
            if user:
                if user.Password==password and user.Role=="Doctor":
                    doc = Doctor.objects.get(user_id=user)
                    request.session['Email'] = user.Email
                    request.session['Role'] = user.Role
                    request.session['id'] = user.id
                    request.session['Firstname'] = doc.Firstname
                    request.session['Lastname'] = doc.Lastname
                    return redirect('ddashboard')
                else:
                    message = "Password-Email does not match!!"
                    return render(request,"app/doctor-login.html",{'msg':message})
            else:
                message = "Email does not Exits!!!"
                return render(request,"app/doctor-login.html",{'msg':message})

        elif request.POST['role']=="Patient":
            email = request.POST['email']
            password = request.POST['pass']

            user =User.objects.get(Email=email)
            if user:
                if user.Password==password and user.Role=="Patient":
                    pat =Patient.objects.get(user_id=user)
                    request.session['Firstname'] = pat.Firstname
                    request.session['Lastname'] = pat.Lastname
                    request.session['Email'] = user.Email
                    request.session['Role'] = user.Role
                    request.session['id'] = user.id
                    return redirect('pdashboard')
                else:
                    message = "Password-Email does not match"
                    return render(request,"app/patient-login.html",{'msg':message})
            else:
                message = "Email does not Exits!!!"
                return render(request,"app/patient-login.html",{'msg':message})

        else:
            if request.POST['role']=="Pharmacy":
                email = request.POST['email']
                password = request.POST['pass']

                user =User.objects.get(Email=email)
                if user:
                    if user.Password==password and user.Role=="Pharmacy":
                        pha =Pharmacy.objects.get(user_id=user)
                        request.session['Fullname'] = pha.FullName
                        request.session['Pharmaname'] = pha.PharmaName
                        request.session['Email'] = user.Email
                        request.session['Role'] = user.Role
                        request.session['id'] = user.id
                        uid = request.session['id']
                        pid = Pharmacy.objects.get(user_id = uid)
                        pro = Product.objects.filter(pharmacy_id=pid)
                        cost = 0
                        for j in pro:
                            cost += j.Price
                        return render(request,"app/admin/pharmacy-dashboard.html",{'pcount':len(pro),'cost':cost})
                    else:
                        message = "Password-Email doesnot match"
                        return render(request,"app/pharmacy-login.html",{'msg':message})
                else:
                    message = "password doesnot match"
                    return render(request,"app/pharmacy-login.html",{'msg':message})
    except Exception as e:
        print("Regitration exception ------------>",e)

def Home(request):
    uid = request.session['id']
    pid = Pharmacy.objects.get(user_id = uid)
    pro = Product.objects.filter(pharmacy_id=pid)
    
    cost = 0
    order = 0
    earning = 0
    for j in pro:
        orp = Shopping_cart.objects.filter(product_id = j.id)
        for k in orp:
            order += 1
            earning += k.Total
        cost += j.Price
    return render(request,"app/admin/pharmacy-dashboard.html",{'pcount':len(pro),'cost':cost,'order':order,'earn':earning})

def ProfilePage(request,pk):
    udata = User.objects.get(id=pk)
    print("Udata------------>",udata)

    if udata.Role=="Patient":
        pdata = Patient.objects.get(user_id=udata)
        print("Paitemt DATA -------------->",pdata)
        return render(request,"app/patient-profile.html",{"key2":pdata})
    elif udata.Role == "Doctor":
        ddata = Doctor.objects.get(user_id=udata)
        print("Doctor DATA -------------->",ddata)
        return render(request,"app/doctor-profile.html",{"key2":ddata})
    else:
        if udata.Role == "Pharmacy":
            pdata = Pharmacy.objects.get(user_id=udata)
            print("Pharmacy DATA -------------->",pdata)
        return render(request,"app/admin/pharmacyprofile.html",{"key2":pdata})

def UpdateDocData(request,pk):
    udata = User.objects.get(id=pk) 
    if udata.Role=="Doctor":
        doc = Doctor.objects.get(user_id=udata)
        doc.Firstname = request.POST['fname']
        doc.Lastname = request.POST['lname']
        doc.Contact = request.POST['contact']
        doc.Year_of_experience = request.POST['Year_of_experience']
        doc.Specialazion = request.POST['Specialazion']
        doc.address = request.POST['address']
        doc.city = request.POST['city']
        doc.state = request.POST['state']
        doc.Gender = request.POST['Gender']
        doc.birthdate = request.POST['birthdate']
        doc.location = request.POST['location']
        doc.about_doc = request.POST['about_doc']
        doc.designation = request.POST['designation']
        doc.Clinic_name = request.POST['Clinic_name']
        doc.doc_fees = request.POST['fees']
        doc.profile_pic = request.FILES['image']
        doc.save()
        url = f"/profilepage/{pk}"
    return redirect(url)

def UpdatePatData(request,pk):
    udata = User.objects.get(id=pk)
    if udata.Role=="Patient":
        pat = Patient.objects.get(user_id=udata)
        pat.Lastname = request.POST['lname']
        pat.Firstname = request.POST['fname']
        pat.Contact = request.POST['contact']
        pat.Address = request.POST['Address']
        pat.city = request.POST['city']
        pat.state = request.POST['state']
        pat.Gender = request.POST['Gender']
        pat.birthdate = request.POST['birthdate']
        pat.blood_presure = request.POST['blood_presure']
        pat.blood_group = request.POST['blood_group']
        pat.sugar = request.POST['sugar']
        pat.Haemoglobin = request.POST['Haemoglobin']
        pat.profile_pic = request.FILES['image']
        pat.save()
        url = f"/profilepage/{pk}"
    return redirect(url)

def UpdatePhaData(request,pk):
    udata = User.objects.get(id=pk)
    if udata.Role=="Pharmacy":
        pha = Pharmacy.objects.get(user_id=udata)
        pha.PharmaName = request.POST['sname']
        pha.Firstname = request.POST['fname']
        pha.Contact = request.POST['contact']
        pha.Address = request.POST['Address']
        pha.City = request.POST['City']
        pha.State = request.POST['State']
        pha.save()
        url = f"/profilepage/{pk}"
    return redirect(url)

def editpage(request,pk):
    edata = User.objects.get(pk=pk)
    return render(request,"app/doctoredit.html",{'key2':edata})

def ShowAllDoctor(request):
    all_doc = Doctor.objects.all()
    return render(request,"app/Show_Doctors.html",{'key2':all_doc})

def DoctorDecription(request,pk):
    doc = Doctor.objects.get(pk=pk)
    return render(request,"app/doctors-details.html",{'key3':doc})

def Logout(request,pk):
    udata = User.objects.get(id=pk)

    if udata.Role=="Doctor":
        del request.session['Email']
        del request.session['Firstname']
        del request.session['Role']
        del request.session['id']
        return HttpResponseRedirect(reverse('doctorlogin'))
    
    elif udata.Role=="Patient":
        del request.session['Email']
        del request.session['Firstname']
        del request.session['Role']
        del request.session['id']
        return HttpResponseRedirect(reverse('patientlogin'))

    if udata.Role=="Pharmacy":
        del request.session['Email']
        del request.session['Pharmaname']
        del request.session['Role']
        del request.session['id']
        return HttpResponseRedirect(reverse('pharmacylogin'))

def ForgotPassword(request):
    return render(request,"app/Enter_Email.html")

def Enter_Mail(request):
    email = request.POST['email']
    user=User.objects.get(Email=email)
    if user:
        otp = randint(10000,99999)
        email_subject = "Forgot Password Varification"
        sendmail(email_subject, 'Email', email, {'otp': otp})
        return render(request,"app/Otppage.html",{'otp':otp,'email':email})
    else:
        message = "Email does not match"
        return render(request,"app/Enter_Email.html",{'msg':message})


def VerifyOtpForgotPassword(request):
    print("------------1--------------")
    try:
        email=request.POST['email']
        eotp=request.POST['eotp']
        gotp = request.POST['gotp']
        print("Eotp--------------->",eotp)
        print(str(eotp))
        user = User.objects.get(Email=email)
        if user:
            if eotp == gotp and user.Role == "Doctor":
                print("===========2=========")
                message = "otp verified successfully"
                return render(request,"app/Forgot-Password.html",{'msg':message,'email':email})
            elif eotp==gotp and user.Role =="Patient":
                print("===========3=========")
                message = "otp verified successfully"
                return render(request,"app/Forgot-Password.html",{'msg':message,'email':email})
            elif eotp==gotp and user.Role =="Pharmacy":
                print("===========4=========")
                message = "otp verified successfully"
                return render(request,"app/Forgot-Password.html",{'msg':message,'email':email})
        else:
            print("Otp Does Not Match!! ")
    except Exception as e:
        print("OTP Verify Exception-------------->",e)

def Forget_Password(request):
    vemail=request.POST['email']
    vpassword=request.POST['npass']
    vcpassword=request.POST['cpass']

    user=User.objects.get(Email=vemail)
    if vpassword==vcpassword and user.Role=="Doctor":
        user.Password=vpassword
        user.save()
        msg="password changed successfully"
        return render(request,"app/doctor-login.html",{'msg':msg})
    elif vpassword==vcpassword and user.Role=="Patient":
        user.Password=vpassword
        user.save()
        msg="password changed successfully"
        return render(request,"app/patient-login.html",{'msg':msg})
    elif vpassword==vcpassword and user.Role=="Pharmacy":
        user.Password=vpassword
        user.save()
        msg="password changed successfully"
        return render(request,"app/Pharmacy-login.html",{'msg':msg})
    else:
        msg="Password does not match"
        return render(request,"app/Forgot-Password.html",{'msg':msg,'email':vemail})

def Doc_Change_Password(request):
    return render(request,"app/Doctor-change-password.html")

def Doctor_Change_Password(request):
    email = request.POST['email']
    v_old_pass=request.POST['l_old_pass']
    v_new_pass=request.POST['l_new_pass']
    v_new_confirm_pass=request.POST['l_new_confirm_pass']

    user = User.objects.get(Email=email)
    if user.Role == "Doctor": 
        if v_old_pass!=user.Password:
            msg="Old Password Is Incorrect"
            return render(request,'app/Doctor-change-password.html',{'msg':msg})

        elif v_old_pass==v_new_pass:
            msg="Please Enter Different Password"
            return render(request,'app/Doctor-change-password.html',{'msg':msg})
        elif v_new_pass==v_new_confirm_pass:
            user.Password=v_new_pass
            user.save()
            return HttpResponseRedirect(reverse('doctorlogin')) 
        else:
            msg="New Password And Confirm Password Is Not Matched"
            return render(request,'app/Doctor-change-password.html',{'msg':msg})
    else:
         return render(request,'app/Doctor-change-password.html')

def Pat_Change_Password(request):
    return render(request,"app/Patient-Change-Password.html")

def Patient_Change_Password(request):
    email = request.POST['email']
    v_old_pass=request.POST['l_old_pass']
    v_new_pass=request.POST['l_new_pass']
    v_new_confirm_pass=request.POST['l_new_confirm_pass']

    user = User.objects.get(Email=email)
    if user.Role == "Patient": 
        if v_old_pass!=user.Password:
            msg="Old Password Is Incorrect"
            return render(request,'app/Patient-Change-Password.html',{'msg':msg})

        elif v_old_pass==v_new_pass:
            msg="Please Enter Different Password"
            return render(request,'app/Patient-Change-Password.html',{'msg':msg})
        elif v_new_pass==v_new_confirm_pass:
            user.Password=v_new_pass
            user.save()
            return HttpResponseRedirect(reverse('patientlogin')) 
        else:
            msg="New Password And Confirm Password Is Not Matched"
            return render(request,'app/Patient-Change-Password.html',{'msg':msg})
    else:
         return render(request,'app/Patient-Change-Password.html.html')

#  =============== Schedule + Appointment pages view ================== 

def SchedulePage(request):
    return render(request,"app/schedule.html")

def AvailabilityInsert(request,pk):
    udata = User.objects.get(id=pk) 
    
    if udata.Role=="Doctor":
        doctor_id = Doctor.objects.get(user_id=udata)
        avail_date = request.POST['adate']   
        mstart_time = request.POST['mstime']
        status = request.POST['status']
        mend_time = request.POST['metime']
        estart_time = request.POST['estime']
        eend_time = request.POST['eetime']
        morningday = request.POST.getlist('mday')
        eveningday = request.POST.getlist('eday')

        insertavail = availability.objects.create(doctor_id=doctor_id,status=status,avail_date=avail_date,mstart_time=mstart_time,mend_time=mend_time,estart_time=estart_time,eend_time=eend_time,morningday=morningday,eveningday=eveningday)
        message = "Schedule Update SuccessFully"
        return render(request,"app/schedule.html",{'msg':message})

def AppointmentPage(request):   
    return render(request,"app/appointment.html")

def BookAppointmentPage(request):
    return render(request,"app/book-appointment.html")

def ConfirmPay(request):
    return render(request,"app/Confirm_Pay.html")

def CheckOut(request):
    return render(request,"app/CheckOut.html")

def FetchByIdData(request,pk):
    udata = User.objects.get(id=pk)
    try:

        if udata.Role=="Patient":
            pid = Patient.objects.get(user_id=udata)
            d_id = request.POST['docid']
            
            docid = Doctor.objects.get(user_id=d_id)
            print(docid.id)
            print('**********')
            a_id = availability.objects.filter(doctor_id=docid.id)
            for u in a_id:
                a_id = u
            print(a_id)
            return render(request,"app/book-appointment.html",{'p':pid,'d':docid,'a':a_id})
    except:
        msg = 'Sorry Doctor Is Not Available'
        return render(request,"app/doctor_availabel.html",{'p': msg})


def InsertAppintment(request,pk):

    email = request.POST['email']
    user=User.objects.get(Email=email)
    d_id = request.POST['docid']
    print(d_id,"D_id-------------------")
    p_id = request.POST['patientid']
    fname = request.POST['fname']
    lname = request.POST['lname']
    a_id = request.POST['availid']
    bookdat = request.POST['bookdate']
    booktime = request.POST['btime']
    total = request.POST['total']
    docid =  Doctor.objects.get(id=d_id)
    patid =  Patient.objects.get(id=p_id)
    availid = availability.objects.get(id=a_id)

    print('---------------------',patid)
    
    inappint = Appointment.objects.create(doctor_id=docid,patient_id=patid,availability_id=availid,appointment_bookdate=bookdat,appotime=booktime,total=total)
    #email_subject = "Booking Appointment"
    #msg = "Your Appoinment has been booked successfully"
    #sendmailappo(email_subject, 'Appointment-Email', patid.user_id.Email, {'msg': msg,'Firstname': fname, 'Lastname' : lname})
    return  render(request,"app/Confirm_Pay.html",{'allapp':inappint})

def ConfirmAndPay(request):
    udata = User.objects.get(id=request.session['id'])
    if udata.Role=="Patient":
        pat = Patient.objects.get(user_id=udata)
        all_appo = Appointment.objects.get(patient_id=pat)
        print("ALL APPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",all_appo)
        return render(request,"app/Confirm_Pay.html",{'allapp':all_appo})

def SaveBookingSummary(request):
    udata = User.objects.get(id=request.session['id'])
    if udata.Role=="Patient":
        book = Patient.objects.get(user_id=udata)
        doctorname = request.POST['doctorname']
        date = request.POST['date']
        time = request.POST['time']
        generalfees = request.POST['generalfees']
        total = request.POST['total']
        newconfirm = BookingTable.objects.create(doctorname=doctorname,date=date,time=time,generalfees=generalfees,total=total)
        return render(request,"app/CheckOut.html",{'pat':book,'confirm':newconfirm})

def ShowAllPatientAppointment(request):
    udata = User.objects.get(id=request.session['id'])
    doctor_id = Doctor.objects.get(user_id=udata)
    all_appo = Appointment.objects.all().filter(doctor_id=doctor_id,appointment_status = False)
    return render(request,"app/appointment.html",{'key8':all_appo})

def AcceptAppintDoc(request,pk):
    avldata = Appointment.objects.get(id = pk)
    #print("--------------------------------------",avldata)
    if avldata.appointment_status == False:
        avldata.appointment_status = True
        print("before save")
        avldata.save()
        print("after save")
        # email_subject = "Appointment Status"
        # msg = "Your Appoinment has been Accepted!!"
        # sendmailpre(email_subject, 'Appointment-Accept',{'msg': msg})
        return render(request,"app/Case.html",{'key65':avldata})
    else :
        return render(request,"app/doctors-dashboard.html")

def ShowAppointmentpatient(request):
    udata = User.objects.get(id=request.session['id'])
    patient_id = Patient.objects.get(user_id=udata)
    all_appo = Appointment.objects.all().filter(patient_id=patient_id,appointment_status=True)
    return render(request,"app/Patient_Appointment.html",{'key9':all_appo})

def Casepage(request):   
    return render(request,"app/Case.html")

def InsertCase(request,pk):
    p_id = request.POST['patientid']
    print(p_id,"p_id------------------->")
    d_id = request.POST['docid']
    disease = request.POST['disease']
    symptoms = request.POST['symptoms']
    medicine = request.POST['medicine']
    docid =  Doctor.objects.get(id=d_id)
    patid =  Patient.objects.get(id=p_id)
    print('docid--------------------->',docid)
    incase = Case.objects.create(doctor_id=docid,patient_id=patid,disease=disease,symptoms=symptoms,medicine=medicine)
    return render(request,"app/Prescription.html",{'key71':incase})
    #return redirect('prescription')

def ShowPatientCase(request):
    udata = User.objects.get(id=request.session['id'])
    doctor_id = Doctor.objects.get(user_id=udata)
    all_case = Case.objects.all().filter(doctor_id=doctor_id)
    return render(request,"app/Show_Case.html",{'key66':all_case})

def prescription(request):
    return render(request,"app/Prescription.html")

def InsertPriscription(request):
    return redirect('ddashboard')

def SavePrescription(request):
    udata = User.objects.get(id=request.session['id'])
    if udata.Role=="Doctor":
        p_id = request.POST['patientid']
        print(p_id,"p_id------------------->")
        d_id = request.POST['docid']
        attachment_file = request.POST['attachment_file']
        docid =  Doctor.objects.get(id=d_id)
        patid =  Patient.objects.get(id=p_id)
        print('docid--------------------->',docid)
        newpre = Prescription.objects.create(doctorname=doctorname,date=date,time=time,generalfees=generalfees,total=total)
        return render(request,"app/CheckOut.html")

   

# ======================== Admin Page Views ===============================

def Adminpage(request):
    return render(request,"app/admin/index.html")

def AdminLoginPage(request):
    return render(request,"app/admin/Admin-login.html")

def AdminLogin(request):
    uname = request.POST['username']
    password = request.POST['password']

    if uname == "admin" and password == "admin":
        request.session['username'] = uname
        request.session['password'] = password

        return render(request,"app/admin/index.html")
    else:
        message = "username or Password doesnot match"
        return render(request,"app/admin/Admin-login.html",{'msg':message})

def AdminLogout(request):
    del request.session['username']
    return HttpResponseRedirect(reverse('adlogin'))

def AdminDocUserTablePage(request):
    all_doc = Doctor.objects.all()
    return render(request,"app/admin/Doctortable.html",{'key5':all_doc})

def AdminPatUserTablePage(request):
    all_pha = Pharmacy.objects.all()
    return render(request,"app/admin/Pharmacytable.html",{'key5':all_pha})


def AdminDocProfilePage(request,pk):
    ddata = Doctor.objects.get(pk=pk)
    print("Doctor DATA -------------->",ddata)
    return render(request,"app/admin/DoctorProfile.html",{"key7":ddata})

# def AdminPhaProfilePage(request,pk):
#     pdata = Patient.objects.get(pk=pk)
#     print("Patient DATA -------------->",pdata)
#     return render(request,"app/admin/PatientProfile.html",{"key7":pdata})

def AdminDocUpadatePage(request,pk):
    udata = User.objects.get(id=pk) 
    if udata.Role=="Doctor":
        doc = Doctor.objects.get(user_id=udata)
        doc.Firstname = request.POST['fname']
        doc.Lastname = request.POST['lname']
        doc.Contact = request.POST['contact']
        doc.Year_of_experience = request.POST['Year_of_experience']
        doc.Specialazion = request.POST['Specialazion']
        doc.address = request.POST['address']
        doc.city = request.POST['city']
        doc.state = request.POST['state']
        doc.Gender = request.POST['Gender']
        doc.birthdate = request.POST['birthdate']
        doc.location = request.POST['location']
        doc.about_doc = request.POST['about_doc']
        doc.designation = request.POST['designation']
        doc.Clinic_name = request.POST['Clinic_name']
        doc.profile_pic = request.FILES['image']
        doc.save()
        url = f"/admin/DoctorProfile/{pk}"
        return redirect(url)
    # elif udata.Role=="Patient":
    #     pat = Patient.objects.get(user_id=udata)
    #     pat.Lastname = request.POST['lname']
    #     pat.Firstname = request.POST['fname']
    #     pat.Contact = request.POST['contact']
    #     pat.Address = request.POST['Address']
    #     pat.city = request.POST['city']
    #     pat.state = request.POST['state']
    #     pat.Gender = request.POST['Gender']
    #     pat.birthdate = request.POST['birthdate']
    #     pat.blood_presure = request.POST['blood_presure']
    #     pat.blood_group = request.POST['blood_group']
    #     pat.sugar = request.POST['sugar']
    #     pat.Haemoglobin = request.POST['Haemoglobin']
    #     pat.profile_pic = request.FILES['image']
    #     pat.save()
    #     url = f"/admin/PatientProfile/{pk}"
    #     return redirect(url)

def AdminDocPage(request,pk):
    udata = User.objects.get(id=pk) 
    if udata.Role=="Doctor":
        udata = Doctor.objects.get(user_id=udata)
       
    
        udata.is_verified = request.POST['is_verified']
        
       
        udata.save()
        url = f"/admin/DoctorProfile/{pk}"
        return redirect(url)

# ====================== Pharmacy =================== #

def category(request):
    return render(request,"app/admin/category.html")




    # all_pro = Product.objects.all()
    # return render(request,"app/admin/showproduct.html",{'key15':all_pro})

def Addcategory(request):

    Title = request.POST['Title']
    Keywords = request.POST['Keywords']
    Description = request.POST['Description']
    Image = request.FILES['Image']
    
    category = Category.objects.create(Title=Title,Keywords=Keywords,Description=Description,Image=Image)
    return render(request,"app/admin/category.html")

def showcategory(request):
    all_cat = Category.objects.all()
    return render(request,"app/admin/showcategory.html",{'key19':all_cat})

def product(request):
    all_cat = Category.objects.all()
    return render(request,"app/admin/Addproduct.html",{'key9':all_cat})


def AddProduct(request,pk):
    try:
        udata = User.objects.get(id=pk) 
        
        if udata.Role=="Pharmacy":
            ph_id = request.POST['pharmacy_id']
            pharmacy_id = Pharmacy.objects.get(user_id=udata)
            print(pharmacy_id,"pharmacyid-------------------")
            Productname = request.POST['Productname']
            Price  = request.POST['Price']
            ProductDescription = request.POST['ProductDescription']
            Expirydate = request.POST['Expirydate']
            Mfgdate = request.POST['Mfgdate']
            Details = request.POST['Details']
            Image = request.FILES['Image']
            status = request.POST['status']
            Quantity = request.POST['Quantity']
            print('888888888888888888')
            # Category= request.POST['Category']
            print('#@@#')
            product = Product.objects.create(pharmacy_id=pharmacy_id,Productname=Productname,ProductDescription=ProductDescription,Price=Price,Expirydate=Expirydate,Mfgdate=Mfgdate,Details=Details,Quantity=Quantity,Category=Category,Image=Image,status=status)
            url = f"/Showproduct/{pk}"
            return redirect(url)
        #     msg='product added'
        # return render(request,"app/admin/Addproduct.html")
    except Exception as e:
     print("Regitration exception ------------>",e)



def Showallproduct(request,pk):
    print("--------------Before Update ShowProductPage---------------",pk)
    pdata = User.objects.get(id=pk)
    print("======================After Update Show Product Id=======",pdata)
    if pdata.Role == "Pharmacy":
        page_id = Pharmacy.objects.get(user_id=pdata)
        pro = Product.objects.all().filter(pharmacy_id=page_id)
        return render(request,"app/admin/Showproduct.html",{'key15':pro})

def Uppro(request,pk):
    pro = Product.objects.get(pk=pk)
    return render(request,"app/admin/Updateproduct.html",{'key16':pro})

def UpdateProduct(request,pk):
    pdata = Product.objects.get(pk=pk)
    print("============PDATA=================",pdata)
    pdata.Productname = request.POST['Productname']
    pdata.ProductDescription = request.POST['ProductDescription']
    pdata.Price = request.POST['Price']
    pdata.Expirydate = request.POST['Expirydate']
    pdata.Mfgdate = request.POST['Mfgdate']
    pdata.Details = request.POST['Details']
    pdata.Quantity = request.POST['Quantity']
    pdata.status = request.POST['status']
    udata = request.session['id']
    pdata.save()
    url = f"/Showproduct/{udata}"
    print("=================URL================",url)
    return redirect(url)
    
   
    
    #return render(request,"app/admin/Showproduct.html")
   


def DeleteProduct(request,pk):
    ddata = Product.objects.get(pk=pk)
    ddata.delete()
    udata = request.session['id']
    print("===========Product UDATA=================",udata)
    url = f"/Showproduct/{udata}"
    print("=================URL================",url)
    return redirect(url)
   
def orderlist(request):
    return render(request,"app/admin/orderlist.html")


#---------------Customer--------------------#

def ShowProduct(request):
    pro = Product.objects.all()
    return render(request,"app/customer/showproductcust.html",{'key17':pro})


def Homepharmacy(request):
    pro = Product.objects.all() 
    all_cat = Category.objects.all()
    return render(request,"app/customer/homepharmacy.html",{'key19':pro,'key34':all_cat})

def productdes(request,pk):  
   
    pro = Product.objects.all()
    prod = Product.objects.get(pk=pk)
        
   
    return render(request,"app/customer/productdes.html",{'key18':prod,'key19':pro})




def search(request):
    query = request.GET['query']
    pharmacy  = Product.objects.filter(Q(Productname__icontains=query))
    return render(request,"app/customer/search.html",{'pharmacy':pharmacy})


 
def checkout(request):
    return render(request,"app/customer/checkout1.html")

def Addtocart(request,pk):
    udata = User.objects.get(id=pk)
    if udata.Role=="Patient":
        pat = Patient.objects.get(user_id=udata)

        pid = request.POST['proid']
        proid = Product.objects.get(id=pid)
        price = int(request.POST['pprice'])
        cqty = int(request.POST['cqty'])
        proname = request.POST['pname']
        total = price * cqty

        if Shopping_cart.objects.filter(product_id=proid):
            print("Hellooo")
            sc = Shopping_cart.objects.get(product_id=proid)
            
            sc.cartqty +=1
            sc.Total= sc.Price * sc.cartqty
            sc.save()
        else:
            newpro = Shopping_cart.objects.create(patient_id=pat,product_id=proid,cartqty=cqty,Productname=proname,Price=price,Total=total)
                
        url = f"/cartpro/{pk}"
        return redirect(url)
        
        
                   
                       

   
        # udata = User.objects.get(id=request.session['id'])
        # if udata.Role=="Patient":
        #     pat = Patient.objects.get(user_id=udata)

        #     pid = request.POST['proid']
        #     proid = Product.objects.get(id=pid)
        #     carts = Shopping_cart.objects.get(id=pk)

        #     c=Shopping_cart.objects.get(product_id=proid)
        #     if c:
        #         cqty=+1
                
        #         total = price * cqty
        #         url = f"/cartpro/{pk}"
        #         return redirect(url)

        #     else:
        #         price = int(request.POST['pprice'])
        #         cqty = int(request.POST['cqty'])
        #         proname = request.POST['pname']
        #         total = price * cqty
        #         newpro = Shopping_cart.objects.create(patient_id=pat,product_id=proid,cartqty=cqty,Productname=proname,Price=price,Total=total)
                
        #         url = f"/cartpro/{pk}"
        #         return redirect(url)


def CartProduct(request,pk):
    udata = User.objects.get(id=pk)
    sub_total=0
    if udata.Role=="Patient":
        pat = Patient.objects.get(user_id=udata)
        c_pro = Shopping_cart.objects.all().filter(patient_id=pat)
        for t in c_pro:
            sub_total += t.Total
        print(sub_total)
        
        return render(request,"app/customer/addcart.html",{'key21':c_pro,'sub_total':sub_total})
    else:
        print("============ERROR===========")




def change_cqty(request,pk):
    try:
        pdata =Shopping_cart.objects.get(pk=pk)
        print("============PDATA=================",pdata)
        pdata.cartqty = int(request.POST['cartqty'])
        pdata.Total = pdata.Price * pdata.cartqty
        udata = request.session['id']
        
        pdata.save()
        url = f"/cartpro/{udata}"
        print("=================URL================",url)
        return redirect(url)
    except Exception as e:
        print("Regitration exception ------------>",e)

def DeletecartProduct(request,pk):
    try:
        ddata = Shopping_cart.objects.get(pk=pk)
        ddata.delete()
        udata = request.session['id']
        print("===========Product UDATA=================",udata)
        url = f"/cartpro/{udata}"
        return redirect(url)
        
        print("=================URL================",url)

    except Exception as e:
        print("Regitration exception ------------>",e)
    

def Proceedtocheckout(request,pk):
    udata = User.objects.get(id=pk)
    sub_total = 0
    if udata.Role=="Patient":
        cdata = Patient.objects.get(user_id=udata)
        all_data1=Shopping_cart.objects.all().filter(patient_id=cdata)
        for t in all_data1:
            sub_total += t.Total
        return render(request,"app/customer/checkout1.html",{'keyp':all_data1,'keyc':cdata,'sub_total':sub_total})

def feedback_submit(request,pk):
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        if user.Role=="Patient":
            patient = Patient.objects.get(user_id=user)
            pid = request.POST['proid']
            proid = Product.objects.get(id=pid)
            rating = int(request.POST['rating'])
            description = request.POST['description']
            new = Feedback.objects.create(Patient=patient,Product=proid,Rating=rating,Description=description)
            msg="Your Feedback saved succesfully"
            return render(request,"app/customer/feedback.html",{'key18':product,'msg':msg})

def myorder(request):
    return render(request,"app/customer/myorder.html")


#------category page----------------#
def cat1(request):
    Tablet=Product.objects.filter(Category='Tablet')
    return render(request,'app/customer/cat1.html',{'Tablet':Tablet}) 

def Ayurvediccare(request):
    Ayurvediccare=Product.objects.filter(Category='Ayurvediccare')
    return render(request,'app/customer/cat1.html',{'Ayurvediccare':Ayurvediccare})











################################ Other code:#############################

#def FetchByIdDataCase(request,pk):
    # udata = User.objects.get(id=pk)
    # if udata.Role=="Doctor":
    #     d_id = Doctor.objects.get(user_id=udata)
    #     p_id = request.POST['patid']
    #     patid = Patient.objects.get(id=p_id)
    #     return render(request,"app/Case.html",{'p':patid,'d':d_id})
    # try:    
    #     udata = User.objects.get(id=pk)
    #     if udata.Role=="Doctor":
    #         d_id = Doctor.objects.get(user_id=udata)
    #         p_id = request.POST['patid']
    #         patid = Patient.objects.get(id=p_id)
    #         return render(request,"app/Case.html",{'p1':patid,'d1':d_id})
    # except Exception as e:
    #     print("OTP Verify Exception-------------->",e)


# def appointment_resp(request, pk, resp='cancel'):
#     print(pk, resp)
#     udata = User.objects.get(id=pk)

#     avldata = Appointment.objects.get(id = request.session['id'])

#     print(udata)
#     if resp == 'accept':
#         avldata.appointment_status = True
#         return render(request, 'app/Case.html')
#     else:
#         return redirect('/ddashboard')


############################################# Paytm Block #################################################

def initiate_payment(request):
    try:
        udata = User.objects.get(Email=request.session['Email'])
        amount = int(request.POST['total'])
        #user = authenticate(request, username=username, password=password)
    except Exception as err:
        print(err)
        return render(request, 'app/checkout.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=udata, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.Email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'app/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'app/callback.html', context=received_data)
        return render(request, 'app/callback.html', context=received_data)

def welcome(request):
    all_doc = Doctor.objects.all()
    msg = 'Time Out'
    return render(request,"app/Show_Doctors.html",{'key2':all_doc,'msg':msg})
