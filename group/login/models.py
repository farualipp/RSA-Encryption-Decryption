from django.db import models

class RSAKey(models.Model):
    class Meta:
        app_label = 'login'
    public_key = models.TextField()
    private_key = models.TextField()


# Create your models here.
