from django.db import models


class Guest(models.Model):
    name = models.CharField(max_length=50, default="Ilya")
    sur_name = models.CharField(max_length=50, default="Rybin")
    last_name = models.CharField(max_length=50, default="Vladislavovich")
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Organization(models.Model):
    creator = models.ForeignKey(Guest, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    icon = models.URLField()


class Meeting(models.Model):
    creator = models.ForeignKey(Guest, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    picture = models.URLField()
    place_text = models.CharField(max_length=10000)
    place_link = models.URLField(max_length=10000)
    event_time = models.DateTimeField("event time")
