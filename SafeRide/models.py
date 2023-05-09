from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator

# get user model
User = get_user_model()

# Create your models here.
class UmusareRider(models.Model):
    user = models.OneToOneField(User, verbose_name="User", related_name="rider_profile", on_delete=models.CASCADE)
    phone_number =models.CharField(verbose_name = "Phone Number",blank=True ,max_length=20)
    bank_account =models.CharField(verbose_name = "Bank_Account",max_length=100,blank=True)
    driving_license_category = models.CharField(verbose_name="Category", max_length=10)
    profile_image = models.ImageField(
        verbose_name="Profile Picture", 
        upload_to='profile', 
        validators=[FileExtensionValidator(['.png','.jpg','.jpeg','.pdf'])])
    driving_license= models.ImageField(
        verbose_name="driving_license", 
        upload_to='profile', 
        validators=[FileExtensionValidator(['.png','.jpg','.jpeg','.pdf'])]
    )
    national_id= models.ImageField(
        verbose_name="national_id", 
        upload_to='profile', 
        validators=[FileExtensionValidator(['.png','.jpg','.jpeg','.pdf'])]
    )

    def image(self):
        return mark_safe('<img src="/../../media/%s" width="70" />' % (self.profile_image))
    image.allow_tags = True 
    def __str__(self):
        return '{} {}'.format(self.user.first_name,self.user.last_name)

    

class Task(models.Model):
    class Status(models.TextChoices):
        SELECT = "", "Select status"
        PENDING = "pending", "pending"
        PAYED = "complete", "complete"
    rider = models.ForeignKey(UmusareRider, related_name="tasks", on_delete=models.CASCADE)
    request = models.ForeignKey('ClientRequest', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    def __str__(self):
        return self.title



class Journey(models.Model):
    task = models.OneToOneField(Task, related_name="journey",on_delete=models.CASCADE)
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()
    starting_point = models.DateTimeField()
    ending_point = models.DateTimeField()
    
    def __str__(self):
        return self.task



class Services(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return self.name
    


class UmusareWage(models.Model):
    class Status(models.TextChoices):
        SELECT = "", "Select status"
        PENDING = "pending", "pending"
        PAYED = "payed", "payed"
    rider = models.ForeignKey(UmusareRider, related_name="wages", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name="STATUS", choices=Status.choices, default= Status.PENDING, max_length=10)
    def __str__(self):
        return  '{} {}'.format(self.rider,self.amount)



class Clients(models.Model):
    user = models.OneToOneField(User, verbose_name="User", related_name="client_profile", on_delete=models.CASCADE)
    phone_number = models.CharField(verbose_name = "Phone Number",blank=True,max_length=20)
    def __str__(self):
        return '{} {}'.format(self.user.first_name,self.user.last_name)



class ClientProperty(models.Model):
    class CarTransmission(models.TextChoices):
        SELECT = "", "Select car_propery"
        AUTOMATIC = "automatic", "automatic"
        MANUAL = "manual", "manual"
    Client = models.ForeignKey(Clients, related_name="client_vehicles",on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=50)
    car_type = models.CharField(verbose_name="car_type", choices=CarTransmission.choices, default= CarTransmission.SELECT, max_length=10)
    def __str__(self):
        return  '{} {}'.format(self.rider,self.amount)


class ClientRequest(models.Model):
    class RequestStatus(models.TextChoices):
        SELECT = "", "Select status"
        PENDING= "pending", "pending"
        CONFIRMED = "confirmed", "confirmed"
    UmusareRider= models.ForeignKey(UmusareRider, related_name="client_requests",on_delete= models.CASCADE)
    Clients = models.ForeignKey(Clients, related_name="requests",on_delete= models.CASCADE)
    ClientProperty = models.ForeignKey(ClientProperty,on_delete=models.CASCADE) 
    destitation =models.CharField(max_length=250)
    created_request = models.DateTimeField()
    status= models.CharField(verbose_name="STATUS", choices=RequestStatus.choices, default=RequestStatus.PENDING, max_length=10)

    
    