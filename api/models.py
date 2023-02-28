import inspect
import sys
# from django.contrib.auth.models import User
from django.db import models


class Sale(models.Model):
    sale_id = models.IntegerField(primary_key=True)
    date = models.DateField()
    count_pizza = models.IntegerField()
    count_drink = models.IntegerField()
    price = models.IntegerField()
    user_id = models.CharField(max_length=6, null=True)

    class Meta:
        get_latest_by = 'date'

    def __str__(self):
        return '%d: %s' % (self.sale_id, self.price)


class Detail(models.Model):
    sale_id = models.ForeignKey(to=Sale, on_delete=models.CASCADE, related_name='details')
    good = models.CharField(max_length=30)
    price = models.IntegerField()
    date = models.DateField()
    user_id = models.CharField(max_length=6)

    class Meta:
        get_latest_by = 'date'

    def __str__(self):
        return '%d: %s' % (self.sale_id.sale_id, self.good)


model_string_map = {}
for cls_name, cls_obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(cls_obj):
        model_string_map.update({cls_name: cls_obj})

