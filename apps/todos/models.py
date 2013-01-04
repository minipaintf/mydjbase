from django.db import models

# Create your models here.

class Todo(models.Model):
	"""docstring for Todo"""
	created_date = models.DateTimeField('date created')
	updated_date = models.DateTimeField('date updated')