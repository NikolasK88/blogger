from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creating and saves a new user with email and password"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    ROLE_CHOICES = (
        ('blogger', _('Блогер')),
        ('business', _('Бизнес')),
        ('staff', _('Администратор')),
    )

    email = models.EmailField(max_length=255, unique=True)
    user_role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='blogger', null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class BloggerAccount(models.Model):
    user = models.OneToOneField(User, related_name='blogger_user',
                                on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    sex = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    places = models.ManyToManyField('Place', blank=True)
    languages = models.ManyToManyField('Language', blank=True)
    specializations = models.ManyToManyField('Specialization', blank=True)
    is_conditions_accepted = models.BooleanField(default=False)
    is_inst_connected = models.BooleanField(default=False)
    is_fb_connected = models.BooleanField(default=False)
    is_youtube_connected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'BloggerAccount'
        verbose_name_plural = 'BloggerAccounts'

    def __str__(self):
        return str(self.id)


class BusinessAccount(models.Model):
    user = models.OneToOneField(User, related_name='business_user',
                                on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    inst_link = models.CharField(max_length=255, null=True, blank=True)
    fb_link = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'BusinessAccount'
        verbose_name_plural = 'BusinessAccounts'

    def __str__(self):
        return str(self.id)


class Place(models.Model):
    # user = models.ForeignKey(User, related_name='user_place',
    #                          on_delete=models.CASCADE, null=True, blank=True)
    # offer = models.ForeignKey(Offer, related_name='offer_place',
    #                          on_delete=models.CASCADE, null=True, blank=True)
    country_city = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'

    def __str__(self):
        return str(self.id)


class Language(models.Model):
    # user = models.ForeignKey(User, related_name='user_language',
    #                          on_delete=models.CASCADE, null=True, blank=True)
    # offer = models.ForeignKey(Offer, related_name='offer_language',
    #                          on_delete=models.CASCADE, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return str(self.id)


class Specialization(models.Model):
    # user = models.ForeignKey(User, related_name='user_specialization',
    #                          on_delete=models.CASCADE, null=True, blank=True)
    # offer = models.ForeignKey(Offer, related_name='offer_language',
    #                          on_delete=models.CASCADE, null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Specialization'
        verbose_name_plural = 'Specializations'

    def __str__(self):
        return str(self.id)


class Youtube(models.Model):
    user = models.ForeignKey(User, related_name='user_youtube',
                             on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Youtube channel'
        verbose_name_plural = 'Youtube channels'

    def __str__(self):
        return str(self.id)


class Instagram(models.Model):
    user = models.ForeignKey(User, related_name='user_instagram',
                             on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Instagram'
        verbose_name_plural = 'Instagrams'

    def __str__(self):
        return str(self.id)


class Facebook(models.Model):
    user = models.ForeignKey(User, related_name='user_facebook',
                             on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Facebook page'
        verbose_name_plural = 'Facebook pages'

    def __str__(self):
        return str(self.id)

