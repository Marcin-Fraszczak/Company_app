"""
For coverage run:

	pytest --cov-report term:skip-covered --cov-report term-missing --cov
	pytest --cov-report term-missing --cov
	pytest --cov
"""
import pytest
from django.contrib.auth import get_user_model


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