from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:  # 10MB
        raise ValidationError("Maximum file size is 10MB")


class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(
        max_length=500, 
        blank=True,        
    )
    friends = models.ManyToManyField(
        'self', 
        blank=True,
        symmetrical=True,
        related_name="friend_profiles"
    )

    #перевірка на дружбу
    def isFriend(self, username):
        try:
            user_to_check = User.objects.get(username=username)
            return self.friends.filter(user=user_to_check).exists()
        except User.DoesNotExist:
            return False
        

    #метод для отримання фото даного профілю за якийсь період часу,
    #якщо any то буде без фільтру по часу
    def get_recent_photos(self, days=1):
        
        if days=='any':
            return self.photos.filter(
                is_active=True
            )
        else:
            recent_threshold = timezone.now() - timedelta(days=days)
            return self.photos.filter(
                upload_date__gte=recent_threshold,
                is_active=True
            )


class ProfilePhoto(models.Model):
    PHOTO_TYPES = [
        ('GALLERY', 'Gallery Photo'),
        ('AVATAR', 'Profile Avatar'),
    ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    image = models.ImageField(
        upload_to='images/',
        validators=[validate_file_size],
        help_text='Завантажте вашу фотографію(максимальний розмір 10МБ)'
    )
    photo_type = models.CharField(
        max_length=10,
        choices=PHOTO_TYPES,
        default='GALLERY'
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text='Додайте опис своїй фотографії'
    )
    is_active = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-upload_date']
        indexes = [
            models.Index(fields=['photo_type']),
            models.Index(fields=['upload_date']),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



#profile creation on creation of default user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

################################################