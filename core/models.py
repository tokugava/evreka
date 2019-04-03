import uuid
import os
import io
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from django.conf.urls.static import static
from django.core.files.storage import default_storage as storage
 
class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
       Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
 
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
 
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)
 
def scramble_uploaded_filename(instance, filename):
    """
    Scramble / uglify the filename of the uploaded file, but keep the files extension (e.g., .jpg or .png)
    :param instance:
    :param filename:
    :return:
    """
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)
 
def scramble_uploaded_filename_thumb(instance, filename):
    """
    Scramble / uglify the filename of the uploaded file, but keep the files extension (e.g., .jpg or .png)
    :param instance:
    :param filename:
    :return:
    """
    extension = filename.split(".")[-1]
    filename = "{}_thumb.{}".format(uuid.uuid4(), extension)
    return (filename, "{}/{}".format(settings.MEDIA_ROOT, filename))
 
# creates a thumbnail of an existing image
def create_thumbnail(input_image, thumbnail_size=(256, 256)):
    # make sure an image has been set
    if not input_image or input_image == "":
        return
 
    # open image
    image = Image.open(input_image)
 
    # use PILs thumbnail method; use anti aliasing to make the scaled picture look good
    image.thumbnail(thumbnail_size, Image.ANTIALIAS)
 
    # parse the filename and scramble it
    filename_base, filename_ext = os.path.splitext(input_image.name)
    (filename, path) = scramble_uploaded_filename_thumb(None, os.path.basename(input_image.name))
    # add _thumb to the filename
 
    # save the image in MEDIA_ROOT and return the filename
    f_thumb = storage.open(filename, "wb")
    sfile = io.BytesIO()
    ext = filename_ext[1:]
    ext = 'JPEG' if ext.lower() == 'jpg' else ext.upper()
    image.save(sfile, ext)
    f_thumb.write(sfile.getvalue())
    f_thumb.close()
    return filename
 
class Site(models.Model):
    site_name = models.CharField(max_length=25)
    address = models.CharField(max_length=500)
    client_id = models.CharField(max_length=100, null=True)
 
    def __str__(self):
        return self.site_name
 
class Site_User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    block_id = models.CharField(max_length=25, null=True)
    apartment_id = models.IntegerField(null=True)
 
    USERNAME_FIELD = 'email'
    objects = MyUserManager()
 
    def __str__(self):
       return self.email
 
    def get_full_name(self):
        return self.email
 
    def get_short_name(self):
        return self.email
 
class Public_Message(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.CharField(max_length=10000)
    message_type = models.CharField(max_length=10)
    publish_date = models.DateTimeField('date published')
    expire_date = models.DateTimeField('date to expire')
   
    def __str__(self):
        return self.subject
   
class Poll_Choice(models.Model):
    question = models.ForeignKey(Public_Message, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.question.subject + ' ' + self.choice_text
   
class User_Choice(models.Model):
    question = models.ForeignKey(Public_Message, on_delete=models.CASCADE)
    choice = models.ForeignKey(Poll_Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(Site_User, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.user.email + ' ' + self.choice.choice_text
   
class Private_Message(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.CharField(max_length=10000)
    from_user = models.ForeignKey(Site_User, related_name='from_users', on_delete=models.DO_NOTHING)
    to_user = models.ForeignKey(Site_User, related_name='to_users', on_delete=models.DO_NOTHING)
    send_date = models.DateTimeField(auto_now=True)
       
    def __str__(self):
        return self.subject
 
class Public_Image(models.Model):
    question = models.ForeignKey(Public_Message, on_delete=models.CASCADE)
    image = models.ImageField("Uploaded image", upload_to=scramble_uploaded_filename)
    thumbnail = models.ImageField("Thumbnail of uploaded image", blank=True)
 
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # generate and set thumbnail or none
        self.thumbnail = create_thumbnail(self.image)
 
        super(Public_Image, self).save()
 
class Private_Image(models.Model):
    question = models.ForeignKey(Private_Message, on_delete=models.CASCADE)
    image = models.ImageField("Uploaded image", upload_to=scramble_uploaded_filename)
    thumbnail = models.ImageField("Thumbnail of uploaded image", blank=True)
 
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # generate and set thumbnail or none
        self.thumbnail = create_thumbnail(self.image)
 
        super(Private_Image, self).save()