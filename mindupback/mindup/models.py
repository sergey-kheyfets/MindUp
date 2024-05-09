from django.db import models


class Guest(models.Model):
    name = models.CharField(max_length=50, default="Ilya")
    sur_name = models.CharField(max_length=50, default="Rybin")
    last_name = models.CharField(max_length=50, default="Vladislavovich")
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def to_dict(self):
        return {
            'name': self.name,
            'sur_name': self.sur_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'pub_date': self.pub_date.strftime('%Y-%m-%d %H:%M:%S')
        }


class Organization(models.Model):
    creator = models.ForeignKey(Guest, on_delete=models.SET_DEFAULT, default=1)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=10000, default="-")
    icon = models.CharField(max_length=200, default="-")
    members = models.ManyToManyField(Guest, related_name='organization_members_set')

    def to_dict(self):
        return {'creator': self.creator.id,
                'title': self.title,
                'description': self.description,
                'icon': self.icon}


class Meeting(models.Model):
    creator = models.ForeignKey(Guest, on_delete=models.SET_DEFAULT, default=1)
    organization = models.ForeignKey(Organization, on_delete=models.SET_DEFAULT, default=1)

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=10000, default="-")
    picture = models.CharField(max_length=200, default="-")
    place_text = models.CharField(max_length=10000, default="-")
    place_link = models.URLField(max_length=10000, default="-")
    event_time = models.DateTimeField("event time")
    members = models.ManyToManyField(Guest, related_name='meeting_members_set')

    def to_dict(self):
        return {
            'creator': self.creator.id,
            'organization': self.organization.id,
            'title': self.title,
            'description': self.description,
            'picture': self.picture,
            'place_text': self.place_text,
            'place_link': self.place_link,
            'event_time': self.event_time.strftime('%Y-%m-%d %H:%M:%S')
        }
