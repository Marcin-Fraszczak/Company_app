"""
For coverage run:

	pytest --cov-report term:skip-covered --cov-report term-missing --cov
	pytest --cov-report term-missing --cov
	pytest --cov
"""
import pytest
from django.contrib.auth import get_user_model


class TestSuperuserCommand:
	User = get_user_model()
	@pytest.mark.django_db
	def test_superuser_command_adding_user(self):
		admin_username = "admin"
		users_before = self.User.objects.all().count()
		self.User.objects.create_superuser(
			username=admin_username,
			password='Testpass123#',
			email='a@a.pl',
			first_name='first',
			last_name='last'
		)
		users_after = self.User.objects.all().count()
		assert users_after - users_before == 1
		user = self.User.objects.get(username=admin_username)
		assert user

	@pytest.mark.django_db
	def test_superuser_not_created_without_admin_privileges(self):
		users_before = self.User.objects.all().count()
		admin_privileges = ["is_staff", "is_superuser", "is_active"]
		for privilege in admin_privileges:
			try:
				self.User.objects.create_superuser(
					username="admin",
					password='Testpass123#',
					email='a@a.pl',
					first_name='first',
					last_name='last',
					is_staff=privilege!="is_staff",
					is_superuser=privilege!="is_superuser",
					is_active=privilege!="is_active"
				)
			except ValueError:
				pass
			finally:
				users_after = self.User.objects.all().count()
				assert users_after - users_before == 0


class TestUserModel:
	User = get_user_model()
	@pytest.mark.django_db
	def test_user_print_representation(self):
		first, last = "first", "last"
		username = "test_user"
		self.User.objects.create(
			username=username,
			password='Testpass123#',
			email='a@a.pl',
			first_name='first',
			last_name='last',
		)
		user = self.User.objects.get(username=username)
		assert str(user) == f"{first} {last}"