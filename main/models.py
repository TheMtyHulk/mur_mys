from django.db import models

# Create your models here.
class Murders(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='murders/')
    date= models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
class suspects(models.Model):
    murders= models.ForeignKey(Murders, on_delete=models.CASCADE, related_name='suspects')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='suspects/', null=True, blank=True)
    def __str__(self):
        return self.name

class investigators(models.Model):
    murders = models.ForeignKey(Murders, on_delete=models.CASCADE, related_name='investigations')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='investigations/', null=True, blank=True)
    def __str__(self):
        return self.name

class interviews(models.Model):
    murders = models.ForeignKey(Murders, on_delete=models.CASCADE, related_name='interviews')
    suspects = models.ForeignKey(suspects, on_delete=models.CASCADE, related_name='interviews')
    investigators = models.ForeignKey(investigators, on_delete=models.CASCADE, related_name='interviews')
    content = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='interviews/', null=True, blank=True)
    def __str__(self):
        return f"Interview with {self.suspects.name} by {self.investigators.name}"

    