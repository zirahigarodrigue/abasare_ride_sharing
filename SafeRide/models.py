from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator

# get user model
User = get_user_model()

# Create your models here.
class UmusareRider(models.Model):
    class Gender(models.TextChoices):
        SELECT = "", "Select Gender"
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    gender = models.CharField(verbose_name="Gender", choices=Gender.choices, default=Gender.SELECT, max_length=10)
    phone_number = PhoneNumberField(verbose_name = "Phone Number",blank=True, unique=True)
    bank_account =models.NumberField(verbose_name = "Bank_Account",blank=True, unique=True)
    age= models.CharField(verbose_name="Age", max_length=10)
    national_id=models.NumerField(verbose_name = "National Id",blank=True, unique=True)
    driving_license_category = models.CharField("Category", verbose_name="Category", max_length=10)
    profile_image = models.ImageField(
        verbose_name="Profile Picture", 
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
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
   

    def __str__(self):
        return self.title
    
    
