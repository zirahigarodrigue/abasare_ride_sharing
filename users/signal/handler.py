from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
User = get_user_model()

from SafeRide.models import UmusareRider, Clients


@receiver(post_save,sender=User)
def create_umusare_or_client(sender,**kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        if user.is_vehicle_owner == True:
            Clients.objects.create(user=user, phone_number='')
        elif user.is_umusare_rider == True:
            UmusareRider.objects.create(
                user=user, 
                phone_number='', 
                bank_account='', 
                driving_license_category='', 
                profile_image='', 
                driving_license='', 
                national_id='',
            )