from django.contrib.auth import get_user_model
from django.db import models

STATUS_CHOICES = (
	("1", "Planning"),
	("2", "Accepted"),
	("3", "In Execution"),
	("4", "Finished"),
	("5", "Archived"),
)


class Project(models.Model):
	name = models.CharField(max_length=128)
	created_date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=128, choices=STATUS_CHOICES, default='1')
	created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

	def __str__(self):
		return self.name
