from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.db import models
from users.exceptions import NoFirstName, NoLastName


class CustomUserManager(BaseUserManager):
	def create_user(self, username, email, password, **extra_fields):
		if not 'first_name' in extra_fields:
			raise NoFirstName()
		if not 'last_name' in extra_fields:
			raise NoLastName()
		email = self.normalize_email(email)
		user = self.model(
			username=username,
			email=email,
			**extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		if extra_fields.get('is_active') is not True:
			raise ValueError('Superuser must have is_active=True.')
		return self.create_user(username, email, password, **extra_fields)


username_validator = UnicodeUsernameValidator()


class CustomUser(AbstractUser):
	username = models.CharField(
		"username",
		max_length=150,
		unique=True,
		help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
		validators=[username_validator, MinLengthValidator(3)],
		error_messages={
			"unique": "A user with that username already exists.",
		},
	)
	first_name = models.CharField(
		"first name",
		max_length=150,
		blank=True,
		validators=[MinLengthValidator(3)]
	)
	last_name = models.CharField(
		"last name",
		max_length=150,
		blank=True,
		validators=[MinLengthValidator(3)]
	)

	def __str__(self):
		return f"{self.first_name} {self.last_name}"

	objects = CustomUserManager()

	REQUIRED_FIELDS = ["first_name", "last_name", "email"]
