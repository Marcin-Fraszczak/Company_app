from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.db import models
from users import exceptions
from re import sub as re_sub


class CustomUserManager(BaseUserManager):
	def normalize_email(self, email):
		try:
			# 1.  Trim whitespace from both ends of the address.
			# 2.  Lowercase the address.
			# 3.  Find the local part of the email and the domain.
			email_name, domain_part = email.strip().lower().rsplit("@", 1)
			# 4.  Trim the whitespace from the domain.
			# 5.  Trim any number of periods from the end of the domain.
			domain_part = domain_part.lstrip().rstrip('.')
			# 6.  Convert international domain names to ASCII.
			# domain_part = domain_part.encode("idna")
			# 7.  Check for common typos.
			"""not implemented"""
			# 8.  Remove repetitions of '.com'.
			# 9.  Remove any characters after '.com'.
			re_sub('\.com[a-z0-9]+', '.com', domain_part)
			# 10. Remove leading digits in 'gmail.com'.
			re_sub('[0-9]+gmail.com', 'gmail.com', domain_part)
			# 11. For fastmail.com replace the email local part with the subdomain.
			"""not implemented"""
			# 12. Remove alias parts from the local part.
			"""not implemented"""
			# 13. Put the local part and the domain part back together.
			email = f"{email_name}@{domain_part}"
			# 14. Calculate the MD5 hash.
			"""not implemented"""
			return email
		except ValueError:
			return exceptions.InvalidEmail()

	def create_user(self, username, email, password, is_active=False, **extra_fields):
		if not 'first_name' in extra_fields:
			raise exceptions.NoFirstName()
		if not 'last_name' in extra_fields:
			raise exceptions.NoLastName()
		email = self.normalize_email(email)
		user = self.model(
			username=username,
			email=self.normalize_email(email),
			is_active=is_active,
			**extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
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
