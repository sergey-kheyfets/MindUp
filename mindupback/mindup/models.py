from django.db import models


class Guest(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Organization(models.Model):
    title = models.CharField(max_length=200)
    icon = models.URLField()


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    organisation = models.ForeignKey(Organization, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    icon = models.URLField()
