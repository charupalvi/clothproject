from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Cloth(models.Model):
    name=models.CharField(max_length=40)
    category=models.CharField(max_length=40)
    brand=models.CharField(max_length=40)
    price=models.FloatField()
    quantity=models.IntegerField()
    size=models.IntegerField()
    details=models.CharField(max_length=100)
    imagepath=models.ImageField(upload_to='image',default='')

class Cart(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    clothid = models.ForeignKey(Cloth,on_delete=models.CASCADE,db_column='clothid')
    quantity = models.IntegerField(default=1) 

class Profile(models.Model):
    id=models.ForeignKey(User,on_delete=models.CASCADE,db_column='id',primary_key=True)
    mobile=models.CharField(max_length=10)
    address=models.TextField(max_length=100)

class Order(models.Model):
    orderid=models.CharField(max_length=100)
    userid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')
    clothid = models.ForeignKey(Cloth,on_delete=models.CASCADE,db_column='clothid')
    quantity = models.IntegerField() 

class Multiimage(models.Model):
    clothid = models.ForeignKey(Cloth,on_delete=models.CASCADE,db_column='clothid')
    imagepath=models.ImageField(upload_to='image',default='')


    