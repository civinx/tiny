from django.db import models
from api.utility import gen, star_with_http, delete_http


class Record(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    tiny_url = models.CharField(max_length=5, blank=True)
    old_url = models.CharField(max_length=500)

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        # 存入数据库时，统一删去http开头，防止同一个网站用http/https生成不同的短网址
        self.old_url = delete_http(self.old_url)

        # 如果原网址已经存在，那不修改数据库，直接返回
        if Record.objects.filter(old_url=self.old_url).__len__() != 0:
            return

        # 将不带短网址的record先插入数据库，获得主键
        super(Record, self).save(*args, **kwargs)

        # 用生成的主键映射成短网址
        Record.objects.filter(id=self.id).update(tiny_url=gen(self.id))

