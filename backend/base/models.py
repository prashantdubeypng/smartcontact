from django.db import models

class CustomUser(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def __str__(self):
        return self.name

# contact model to store user contacts
# Each contact is associated with a CustomUser
class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    relationship = models.CharField(max_length=50, blank=True, null=True)
    ispublic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'phone')  # Ensures phone is unique per user

    def __str__(self):
        return f"{self.name} ({self.phone})"

# Interaction model to track interactions between users and contacts
class Interaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} ↔ {self.contact.name}"
