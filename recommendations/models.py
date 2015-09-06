from django.db import models


class FBUser(models.Model):
	fb_id = models.BigIntegerField(primary_key=True)


class UserKeyword(models.Model):
	user = models.ForeignKey(FBUser)
	text = models.CharField(max_length=255)
	relevancy = models.FloatField()
