from django.db import models
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_reviews')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('author', 'recipient')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review from {self.author.name} to {self.recipient.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_recipient_rating()

    def delete(self, *args, **kwargs):
        recipient = self.recipient
        super().delete(*args, **kwargs)
        self.update_recipient_rating(recipient)

    def update_recipient_rating(self, recipient=None):
        recipient = recipient or self.recipient
        avg_rating = Review.objects.filter(recipient=recipient).aggregate(Avg('rating'))['rating__avg']
        
        if recipient.is_customer:
            recipient.customer.rating = avg_rating or 0.0
            recipient.customer.save()
        elif recipient.is_executor:
            recipient.executor.rating = avg_rating or 0.0
            recipient.executor.save()

@receiver(post_save, sender=Review)
def update_rating_on_save(sender, instance, **kwargs):
    instance.update_recipient_rating()

@receiver(post_delete, sender=Review)
def update_rating_on_delete(sender, instance, **kwargs):
    instance.update_recipient_rating(instance.recipient)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.name}"
    
    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/static/images/default-avatar.jpg'
    

class PortfolioImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='portfolio_images')
    image = models.ImageField(upload_to='portfolio/')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.title} for {self.profile.user.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 1000 or img.width > 1000:
                output_size = (1000, 1000)
                img.thumbnail(output_size)
                img.save(self.image.path, quality=70)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()