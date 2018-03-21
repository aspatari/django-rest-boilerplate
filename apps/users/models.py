import importlib

import sys
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework_jwt.settings import api_settings

from apps.common.models import BaseModel
from apps.common.utils import get_time_with_offset
from apps.users.utils import GenericAction
from . import utils


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('The given password must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        """Create and return a `User` with an email, username and password."""

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """
            Create and return a `User` with superuser powers.

            Superuser powers means that this use is an admin that can do anything
            they want.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(
        _('username'),
        max_length=150,
        db_index=True,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(_('email address'), db_index=True, unique=True, blank=True)

    # When a user no longer wishes to use our platform, they may try to delete
    # there account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. To solve this problem, we
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(_('active'), default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users, this flag will always be
    # false.
    is_staff = models.BooleanField(_('staff'), default=False)

    # The `is_confirmed` flag is expected by Django to determine who can and cannot
    # login.
    is_confirmed = models.BooleanField(_('confirmed'), default=False)

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the email field.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.username

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        token_prefix = api_settings.JWT_AUTH_HEADER_PREFIX

        return f"{token_prefix} {self._generate_jwt_token()}"

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def _generate_jwt_token(self) -> str:
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set by setting params.
        """

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)

        return token

    def create_transaction(self, action: str):
        """
        Create a transaction for current user
        :param action: Action name
        :return: Transaction
        """
        transaction = Transaction.objects.create(action=action, user=self)
        return transaction


class Profile(BaseModel):
    GENDERS = (
        ('male', _('Male')),
        ('female', _('Female'))
    )
    # As mentioned, there is an inherent relationship between the Profile and
    # User models. By creating a one-to-one relationship between the two, we
    # are formalizing this relationship. Every user will have one -- and only
    # one -- related Profile model.
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    first_name = models.CharField(_('First Name'), max_length=100, blank=True, null=True)
    last_name = models.CharField(_('Last Name'), max_length=100, blank=True, null=True)
    phone_number = models.CharField(_('Phone Number'), max_length=100, blank=True, null=True)

    gender = models.CharField(_('Gender'), choices=GENDERS, max_length=6, blank=True, null=True)

    # Each user profile will have a field where they can tell other users
    # something about themselves. This field will be empty when the user
    # creates their account, so we specify `blank=True`.
    bio = models.TextField(blank=True)

    # In addition to the `bio` field, each user may have a profile image or
    # avatar. Similar to `bio`, this field is not required. It may be blank.
    image = models.URLField(blank=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.user.username

    def populate_profile(self, validated_data, commit=True):

        # Get model filed list
        fields_list = [field.attname for field in self._meta.fields]

        # Populate fields with incoming data
        for key, value in validated_data.items():
            if key in fields_list:
                setattr(self, key, value)

        if commit:
            # Filter fields for partial update
            updated_fields = list(filter(lambda key: key in fields_list, validated_data.keys()))
            self.save(update_fields=updated_fields)


class Transaction(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    valid_until = models.DateTimeField(_('valid until'))
    action = models.CharField(_('action'), max_length=255)

    # META Fields
    ExpiredTransaction = utils.ExpiredTransaction

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self):
        return f"{self.user.username} {self.action}"

    @property
    def is_valid(self):
        """Check if transaction is not expired """
        current_time = timezone.localtime()
        return current_time <= self.valid_until

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """ Overwrited for automatic  valid_until """
        action_name = self.action.rsplit('.').pop()

        # Magic for taking config parameter by action name
        # Spliting action class name and uppercase it
        action_name_string = "_".join(map(lambda x: x.upper(), utils.camel_case_split(action_name)))

        valid_time = getattr(settings, f'{action_name_string}_VALID_TIME')

        self.valid_until = get_time_with_offset(valid_time)
        super().save(force_insert, force_update, using, update_fields)

    def apply(self, *args, **kwargs):
        """ Method that apply transaction """
        if self.is_valid:
            action = self.get_action(*args, **kwargs)
            action.execute()
        else:
            raise Transaction.ExpiredTransaction

    def get_action(self, *args, **kwargs) -> GenericAction:
        try:
            mod_name, action_name = self.action.rsplit('.', 1)
        except ValueError:
            # If is not founded look in action file for action class
            mod_name = f'{sys.modules[self.__module__].__package__}.actions'
            action_name = self.action
        try:
            mod = importlib.import_module(mod_name)
            action = getattr(mod, action_name)
        except (ModuleNotFoundError, AttributeError):
            print(f"No such module or function <{self.action}>")  # TODO log me
        else:
            return action(self, *args, **kwargs)


@receiver(post_save, sender=get_user_model())
def create_related_profile(sender, instance, created, *args, **kwargs):
    # Notice that we're checking for `created` here. We only want to do this
    # the first time the `User` instance is created. If the save that caused
    # this signal to be run was an update action, we know the user already
    # has a profile.
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)


@receiver(post_save, sender=Transaction)
def apply_transaction_post_create_method(sender, instance, created, *args, **kwargs):
    # Notice that we're checking for `created` here. We only want to do this
    # the first time the `Transaction` instance is created. We execute the `post_create`
    # method for apply logic after transaction is created
    if instance and created:
        action = instance.get_action()
        try:
            action.post_create()
        except AttributeError:
            print(f"Action: <{instance.action}> don't have post_create action or not found")  # TODO log me
