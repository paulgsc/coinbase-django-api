from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField, EncryptedBooleanField, EncryptedDateTimeField, EncryptedIntegerField
from .utlis.utlis import CryptoUtils
from datetime import timedelta
# Create your models here.

class CommonFeatures(models.Model):

    class Meta:
        abstract = True  # This makes it an abstract base model

    @classmethod
    def can_be_featured(cls):
        # You can implement custom logic here to determine if the model can be featured.
        # For example, you can check a global setting or perform other checks.
        return True

# Extend the default user base class.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Please enter a valid phone number")
    phonenumber = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True)
    photoURL = models.URLField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True,
                              default='/placeholder.png')
    last_login_device = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class CoinbaseSupportedScopes(CommonFeatures):
    """
        Model to store all the possible scopes for coinbase supported oauth2.0 scopes
    """
    scope_name = models.CharField(max_length=120, unique=True, validators=[
        RegexValidator(
            regex=r'^wallet:[a-z]+:[a-z]+$',
            message='Scope name must follow the pattern "wallet:<action>:<permission>"',
        )
    ])
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.scope_name


class CoinbaseAPIActions(CommonFeatures):
    """
        Model to store the various actions that a user can grant the coinbase api
    """
    action_name = models.CharField(max_length=60)
    required_scopes = models.ManyToManyField(
        CoinbaseSupportedScopes, related_name='required_actions', blank=True)
    suggested_scopes = models.ManyToManyField(
        CoinbaseSupportedScopes, related_name='suggested_actions', blank=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.action_name
    
class UserCoinbaseGrantedAction(CommonFeatures):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.ForeignKey(
        CoinbaseAPIActions, on_delete=models.CASCADE, related_name='user_actions')
    scopes = models.ManyToManyField(
        CoinbaseSupportedScopes, related_name='user_scopes', blank=True)


class UserCoinBaseAPIKeys(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='coinbase_oauth')
    access_token = EncryptedTextField()
    token_type = EncryptedTextField(max_length=60)
    expires_in = EncryptedIntegerField()
    refresh_token = EncryptedTextField()
    scope = EncryptedTextField(max_length=500)
    updated_at = EncryptedDateTimeField(auto_now=True)

class UserAccessKey(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    access_key = EncryptedCharField(
        max_length=255, unique=True, default=CryptoUtils.generate_encryption_key())
    update_date = models.DateTimeField(auto_now=True)


class CustomPeriodicTask(CommonFeatures):
    class Meta:
        app_label = 'app'

    INTERVAL_CHOICES = [
        ('second', 'Second'),
        ('minute', 'Minute'),
        ('hour', 'Hour'),
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month')
    ]

    name = models.CharField(max_length=60)
    schedule = models.DurationField(default=timedelta(days=1))
    interval_unit = models.CharField(
        max_length=10, choices=INTERVAL_CHOICES, default='day')
    is_site_task = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            # Retrieve the existing instance's name without hitting the database
            existing_instance = CustomPeriodicTask.objects.filter(
                pk=self.pk).only('name').first()

            # Check if the name has been modified
            if existing_instance and existing_instance.name.lower() != self.name.lower():
                raise ValueError(
                    "The 'name' field is immutable and cannot be changed.")

        super().save(*args, **kwargs)