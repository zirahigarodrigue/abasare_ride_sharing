from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator


#added kb
from django.utils import timezone
from decimal import Decimal

# get user model
User = get_user_model()

# Create your models here.
class UmusareRider(models.Model):
    user = models.OneToOneField(User, verbose_name="User", on_delete=models.CASCADE)
    phone_number = models.CharField(verbose_name = "Phone Number",max_length=100,blank=True, unique=True)
    bank_account =models.CharField(verbose_name = "Bank_Account",max_length=100,blank=True, unique=True)
    driving_license_category = models.CharField(verbose_name="Category", max_length=10)
    profile_image = models.ImageField(
        verbose_name="Profile Picture", 
        upload_to='profile', 
        height_field=None, 
        width_field=None, 
        max_length=None,
        validators=[FileExtensionValidator(['png','jpg','jpeg','pdf'])])
    driving_license= models.ImageField(
        verbose_name="driving_license", 
        upload_to='profile', 
        height_field=None, 
        width_field=None, 
        max_length=None,
        validators=[FileExtensionValidator(['png','jpg','jpeg','pdf'])]
    )
    national_id= models.ImageField(
        verbose_name="national_id", 
        upload_to='profile', 
        height_field=None, 
        width_field=None, 
        max_length=None,
        validators=[FileExtensionValidator(['png','jpg','jpeg','pdf'])]
    )

    def image(self):
        return mark_safe('<img src="/../../media/%s" width="70" />' % (self.profile_image))
    image.allow_tags = True 
    def __str__(self):
        return '{} {}'.format(self.user.first_name,self.user.last_name)

    

class Task(models.Model):
    rider = models.ForeignKey(UmusareRider, on_delete=models.CASCADE)
    request = models.ForeignKey('ClientRequest', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    def __str__(self):
        return self.title
    
class Journey(models.Model):
    task = models.OneToOneField(Task,on_delete=models.CASCADE)
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()
    def __str__(self):
        return self.task
    
class Services(models.Model):
    service_name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=6, decimal_places=2)

    # starting_point = models.PointField()
    # ending_point = models.PointField()
    distance = models.FloatField()
    cost_per_km = models.DecimalField(max_digits=8, decimal_places=2)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def calculate_distance(self):
        return self.starting_point.distance(self.ending_point)

    def save(self, *args, **kwargs):
        self.distance = self.calculate_distance()
        if self.cost_per_km and self.distance:
            self.total_cost = self.cost_per_km * self.distance
        super(Services, self).save(*args, **kwargs)

    def __str__(self):
        return f"Route from {self.starting_point} to {self.ending_point} ({self.distance} km, {self.total_cost} cost)"
    

class UmusareWage(models.Model):
    class status(models.TextChoices):
        SELECT = "", "Select status"
        PENDING = "pending", "pending"
        PAYED = "payed", "payed"
    rider = models.ForeignKey(UmusareRider, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name="STATUS", choices=status.choices, default=status.SELECT, max_length=10)

class Clients(models.Model):
    user = models.OneToOneField(User, verbose_name="User", on_delete=models.CASCADE)
    phone_number = models.CharField(verbose_name = "Phone Number",max_length=250,blank=True, unique=True)
    def __str__(self):
        return '{} {}'.format(self.user.first_name,self.user.last_name)

class ClientProperty(models.Model):
    Client = models.ForeignKey(Clients,on_delete=models.CASCADE)
    car_brand = models.CharField(verbose_name="car_brand", max_length=50)
    plate_number = models.CharField(max_length=50)
    vehicle_insurance=models.CharField(max_length=50)



class ClientRequest(models.Model):
    class RequestStatus(models.TextChoices):
        SELECT = "", "Select status"
        PENDING= "pending", "pending"
        DONE = "done", "done"
    #location = models.ForeignKey(Clients,on_delete= models.CASCADE)
    UmusareRider= models.ForeignKey(UmusareRider,on_delete= models.CASCADE)
    Clients = models.ForeignKey(Clients,on_delete= models.CASCADE)
    ClientProperty = models.ForeignKey(ClientProperty,on_delete=models.CASCADE) 
    destitation =models.CharField(max_length=250)
    created_request = models.DateTimeField()
    status= models.CharField(verbose_name="STATUS", choices=RequestStatus.choices, default=RequestStatus.SELECT, max_length=10)

    
    