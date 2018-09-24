from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')

	org = models.CharField('所属组织',max_length=128,blank=True)
	telephone = models.CharField('电话',max_length=50,blank=True)
	mod_date = models.DateTimeField('上次修改时间',auto_now = True)

	class Meta:
		verbose_name = '用户资料'

	def get_absolute_url(self):
		return reverse('myaccount:profile')

	def __str__(self):
		return "{}的资料".format(self.user.__str__())