from django.db import models
from django.contrib.auth.models import User

class Templates(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now_add = True)
    # updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    

class BulkMessages(models.Model):
    TEMPLATE_CHOICES = (
        ('plain_message', 'Plain Message'),
        ('with_image', 'With Image'),
        ('with_document', 'With Document'),
        ('video_message', 'Video Message'),
    )
    
    template = models.ForeignKey(Templates, on_delete=models.DO_NOTHING, blank=True, null=True)
    file = models.FileField(upload_to='bulk_messages/', blank=True, null=True)
    message = models.TextField()
    csv = models.FileField(upload_to='bulk_message_csvs/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.template:
            if self.template.value == 'plain_message' and (self.file or self.image):
                raise ValidationError('Plain messages should not have an image or file.')
            if self.template.value == 'with_image' and not self.file:
                raise ValidationError('With Image template requires an image.')
            if self.template.value == 'with_document' and not self.file:
                raise ValidationError('With Document template requires a document.')
            if self.template.value == 'video_message' and not self.file:
                raise ValidationError('Video Message template requires a video.')

    def __str__(self):
        return self.message


class MessageResponse(models.Model):
    batch = models.ForeignKey(BulkMessages, on_delete=models.DO_NOTHING)
    phone_number= models.CharField(max_length=15)
    response = models.TextField()
    status = models.CharField(max_length=100, default='Failed')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.phone_number

class Sessions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=255, default='menu')
    position = models.CharField(max_length=255, default = 'menu')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
            return ''

class Promotions(models.Model):
    file = models.FileField(upload_to='campaign_messages/')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
            return ''

class Locations(models.Model):
    file = models.FileField(upload_to='locations/')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
            return ''

class MoneyCounter(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='denominations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
            return ''