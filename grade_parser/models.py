from django.db import models

# Create your models here.
class Program(models.Model):
    key = models.IntegerField(primary_key=True)


class KeywordManager(models.Manager):

    def keyword_array(self):
        return self.all().distinct().values_list("text", flat=True)


class Keyword(models.Model):
    program = models.ForeignKey(Program)
    text = models.CharField(max_length=255)
    relevancy = models.FloatField()
    objects = KeywordManager()

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ('text', )
