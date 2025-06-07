from django.db import models

class TimeZone(models.Model):
    time_zone_id = models.AutoField(primary_key=True)
    time_zone_name = models.CharField(max_length=100)

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)

class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    date_time = models.BigIntegerField()
    no_of_slots = models.PositiveIntegerField()
    time_zone_id = models.ForeignKey(TimeZone, on_delete=models.CASCADE)

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
