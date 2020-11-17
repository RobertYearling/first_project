from django.db import models # Should be loaded already
from datetime import date # Need to varify < or > for Date Field
import re # Needed for REGEX

# Create your models here.

class UserManager(models.Manager):
    def registerValidation(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        if len(postData['f_name']) == 0:
            errors['f_name_req'] = "First Name is required!"
        if len(postData['l_name']) == 0:
            errors['l_name_req'] = "Last Name is required!"
        if len(postData['email']) == 0:
            errors['email_req'] = "Email is required!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email_regex'] = "This is an invalid email address"
        if len(postData['pswd']) == 0:
            errors['pswd_req'] = "Password is required!"
        elif len(postData['pswd']) < 8:
            errors['pswd_min'] = "Password must be 8 characters"
        if postData['pswd'] != postData['cfpswd']:
            errors['cfpswd'] = "Passwords Must Match: No Matchie, No Workie"
        return errors

    def loginValidation(self, postData):
        errors = {}

        userEmail = User.objects.filter(email = postData['email'])
        if len(userEmail) == 0:
            errors['emailNF'] = "This email is not found"
        else:
            if userEmail[0].password != postData['pswd']:
                errors['pswdNoMatch'] = "Email or Password incorrect"
        return errors

# ----- End of Registration and Login Validations

class PlannerManager(models.Manager):
    def planValidation(self, postData):
        errors = {}
        today = str(date.today())
        if len(postData['dest']) == 0:
            errors['dest_req'] = "You need to have a Destination"
        if len(postData['desc']) == 0:
            errors['desc_req'] = "You need to have a Description"
        if postData['travel_from'] < today:
            errors['travel_from_req'] = "You need to have a Date"
        if postData['travel_to'] <  postData['travel_from']:
            errors['travel_to_req'] = "Cannot be before Travel Start"
        return errors



# ----- User Models ----- #

class User(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Planner(models.Model):
    destination = models.CharField(max_length=255)
    planner = models.ForeignKey(User, related_name = 'trip_planner', on_delete = models.CASCADE)
    joining = models.ManyToManyField(User, related_name = 'trips_joined')
    decription = models.CharField(max_length=255)
    travel_from = models.DateField()
    travel_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PlannerManager()