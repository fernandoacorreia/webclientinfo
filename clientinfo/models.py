from django.db import models

class Url(models.Model):
    uri = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.uri

class UrlAccess(models.Model):
    url = models.ForeignKey(Url, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.created_on

    def get_access_data(self):
        return self.urlaccessdata_set.order_by('key').all()

class UrlAccessData(models.Model):
    access = models.ForeignKey(UrlAccess, db_index=True)
    key = models.CharField(max_length=60, db_index=True)
    value = models.TextField()
