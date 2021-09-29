from django.db import models

# Create your models here.
class User(models.Model):
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=50)
    Role = models.CharField(max_length=50)
    Otp = models.CharField(max_length=50)
    is_create = models.DateTimeField(auto_now_add=True)
    is_update = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

class Doctor(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    qualification = models.CharField(max_length=100, blank= True)
    Contact = models.BigIntegerField(default=122)
    Year_of_experience = models.IntegerField(default=2)
    Clinic_name = models.CharField(max_length=50)
    Specialazion = models.CharField(max_length=50)
    address = models.CharField(max_length= 500,blank = True)
    city = models.CharField(max_length = 50,default="")
    state = models.CharField(max_length =50, blank= True)
    Gender = models.CharField(max_length=10,default="")
    birthdate = models.DateField(blank=True,default="2021-12-12")
    location = models.CharField(max_length= 30,blank= True)
    about_doc = models.CharField(max_length= 100,blank= True)
    designation = models.CharField(max_length=20,default="")
    profile_pic=models.FileField(upload_to='img/',default='doc_male.png')
    discriptions = models.TextField(max_length=60,default="")
    doc_fees = models.BigIntegerField(default=100)

class Patient(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Contact = models.BigIntegerField(default=10)
    Address = models.CharField(max_length=100)
    Gender = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50,blank=True)
    birthdate = models.DateField(blank=True,default="2021-12-12")

    #updated patiend profile

    blood_group=models.CharField(max_length=10,blank= True)
    blood_presure=models.CharField(max_length=10,blank= True)
    sugar=models.CharField(max_length=10,blank= True)
    Haemoglobin=models.CharField(max_length=10,blank= True)
    profile_pic=models.FileField(upload_to='img/',default='patient_icon.png')

class Pharmacy(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    PharmaName=models.CharField(max_length=50)
    FullName=models.CharField(max_length=50)
    qualification=models.CharField(max_length=100,blank= True)
    InstitutionTrainning=models.CharField(max_length=100,blank= True)
    speciality=models.CharField(max_length=100)
    Countrycode=models.CharField(max_length=30,blank= True)
    Shopname = models.CharField(max_length=50)
    Contact = models.BigIntegerField(default=10)
    Address = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    profile_pic=models.ImageField(upload_to='image/',default='doc_male.png')

class Case(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete = models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Contact = models.BigIntegerField(default=10)
    Address = models.CharField(max_length=100)
    Gender = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    disease = models.CharField(max_length = 100)
    symptoms = models.CharField(max_length = 200)
    medicine = models.TextField(default = 'medicine')
    
class availability(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    avail_date = models.DateField()
    mstart_time = models.TimeField()
    mend_time = models.TimeField()
    estart_time = models.TimeField()
    eend_time = models.TimeField()
    status = models.BooleanField(default= False)
    morningday = models.CharField(max_length=500)
    eveningday = models.CharField(max_length=500)

class Appointment(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete = models.CASCADE)
    availability_id = models.ForeignKey(availability, on_delete = models.CASCADE,default = None)
    appointment_status = models.BooleanField(default= True)
    appointment_bookdate = models.DateField()
    appotime = models.TimeField(default=False)
    payment_status = models.BooleanField(default= False)
    total = models.BigIntegerField(default=50)

class Prescription(models.Model):
    case_id = models.ForeignKey(Case, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    attachment_file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True,blank=False)

class BookingTable(models.Model):
    doctorname = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    generalfees = models.BigIntegerField(default=100)
    total = models.BigIntegerField(default=200) 

# class Payment(models.Model):
#     user_id = models.ForeignKey(User,on_delete=models.CASCADE)
#     email = models.CharField(max_length=200)
#     customer_id = models.CharField(max_length=300)

class Category(models.Model):
    Title = models.CharField(max_length=50) 
    Keywords = models.CharField(max_length=50)
    Description = models.CharField(max_length=50)
    Image = models.ImageField(upload_to="img/")
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    pharmacy_id = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    Productname = models.CharField(max_length=50)
    ProductDescription = models.CharField(max_length=50)
    Price = models.BigIntegerField()
    Expirydate = models.DateField(max_length=50)
    Mfgdate = models.DateField(max_length=50)
    Details = models.CharField(max_length=50)
    Image = models.ImageField(upload_to="img/")
    status = models.BooleanField(default=False)
    Category = models.CharField(max_length=50)
    Quantity  = models.BigIntegerField(default=5)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    pharmacy_id = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    Email = models.EmailField(max_length=50)
    Address = models.CharField(max_length=100)
    Contact = models.BigIntegerField()
    Ordername = models.CharField(max_length=50)
    Total = models.BigIntegerField()
    status =  models.BooleanField(default= False)


# class Faq(models.Model):
    # user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    # Question = models.CharField(max_length=200)
    # Answer = models.CharField(max_length=200)
    # Status = models.CharField(max_length=50)
    # is_created = models.DateTimeField(auto_now_add=True)
    # is_updated = models.DateTimeField(auto_now_add=True)

class Shopping_cart(models.Model):
    patient_id = models.ForeignKey(Patient,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    Productname = models.CharField(max_length=200)
    cartqty = models.BigIntegerField()
    Price = models.BigIntegerField()
    Total = models.BigIntegerField()
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    patient_id = models.ForeignKey(Patient,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    Rating = models.IntegerField(default=0)
    Description = models.TextField(max_length=500)

class Checkout(models.Model):
    
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Total = models.BigIntegerField()
    status =  models.BooleanField(default= False)
    created_at=models.DateTimeField(auto_now_add=True)
    
class Contact(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE,default="")
    FullName = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50)
    Contact = models.BigIntegerField()
    Subject = models.CharField(max_length=50)
    Message = models.CharField(max_length=100)


# class Transaction(models.Model):
#     made_by = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
#     made_on = models.DateTimeField(auto_now_add=True)
#     amount = models.IntegerField()
#     order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
#     checksum = models.CharField(max_length=100, null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if self.order_id is None and self.made_on and self.id:
#             self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
#         return super().save(*args, **kwargs)


class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)