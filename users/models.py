from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from users import exceptions



class CustomUserManager(BaseUserManager):
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


class CustomUser(AbstractUser):
	def __str__(self):
		return f"{self.first_name} {self.last_name}"

	objects = CustomUserManager()
