from __future__ import unicode_literals
import bcrypt
from django.db import models


class UserManager(models.Manager):
	def login(self,post):
		user = self.filter(email=post.get('email')).first()
		if user and bcrypt.hashpw(post.get('password').encode(), user.password.encode()) == user.password:
			return(True,user)
		return(False,'not')

class User(models.Model):
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	birthday = models.DateField()
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Friend(models.Model):
    userfriend = models.ForeignKey(User, related_name='userfriend')
    newfriend= models.ForeignKey(User, related_name='newfriend')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)