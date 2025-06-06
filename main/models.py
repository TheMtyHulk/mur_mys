from django.db import models

# Create your models here.
class Murders(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='murders/')
    date= models.DateTimeField(blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name
class Suspects(models.Model):
    murders= models.ForeignKey(Murders, on_delete=models.CASCADE, related_name='suspects')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='suspects/', null=True, blank=True)
    def __str__(self):
        return self.name

class Investigators(models.Model):
    murders = models.ForeignKey(Murders, on_delete=models.CASCADE, related_name='investigations')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='investigations/', null=True, blank=True)
    def __str__(self):
        return self.name

class Interviews(models.Model):
    murders = models.ForeignKey(Murders, on_delete=models.CASCADE, related_name='interviews')
    suspects = models.ForeignKey(Suspects, on_delete=models.CASCADE, related_name='interviews')
    investigators = models.ForeignKey(Investigators, on_delete=models.CASCADE, related_name='interviews')
    content = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='interviews/', null=True, blank=True)
    def __str__(self):
        suspect_name = self.suspects.name if self.suspects else "Unknown"
        investigator_name = self.investigators.name if self.investigators else "Unknown"
        return f"Interview with {suspect_name} by {investigator_name}"

    