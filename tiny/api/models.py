from django.db import models
from api.utility import gen


class Record(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    tiny_url = models.CharField(max_length=5, blank=True)
    old_url = models.CharField(max_length=500)

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        print(self.old_url)
        print(self.id)
        super(Record, self).save(*args, **kwargs)
        print(self.id)
        Record.objects.filter(id=self.id).update(tiny_url=gen(self.id))

