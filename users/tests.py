import pytest
from django.test import Client
from django.contrib.auth import get_user_model


class TestUserRegistration:
	"""
	Tests all the 'register' endpoint functionalities.
	"""

	@pytest.fixture
	def client(self):
		return Client()

	@pytest.fixture
	def options_response(self, client):
		return client.options(self.register_url)

	register_url = 'http://127.0.0.1:8000/api/accounts/register/'
	user_data = {
		'first_name': 'testuser21',
		'last_name': 'user',
		'username': 'tester',
		'email': 'test@gmail.com',
		'password': 'Testpass123#',
		'password_confirm': 'Testpass123#',
	}
	invalid_passwords = {
		'no capital letter': 'testpass1',
		'no small letter': 'TESTPASS1@',
		'no digit': 'Testpass#',
		'no special sign': 'Testpass1',
		'shorter than 8 characters': 'Testp#1',
		'too common': 'Aaaaaaa1',
		'too similar to email address': '1Test@gmail.com',
		'too similar to first name': 'Testuser21#',
		'too long': '@@#TRkjkwjx11dkjfkjjjjjjjjjjjjjjkowoeiwoeiwoeiwwxlmwkdjwi685094uc9h4iru3h4oucy3ou3yoi4uyoi3'
	}
	invalid_emails = {
		'no @ sign': 'test_gmail.com',
		'too many @ signs': 'te@st@gmail.com',
		'no .sign': 'test@gmailcom',
		'no domain part': 'testgmail.com@',
		'no username part': '@gmail.com',
		'invalid characters in domain part': 'test@#$%^$.12'
	}
	input_lengths = {
		"username": 3,
		"first_name": 3,
		"last_name": 3,
	}
	emails = {
		'normalized': 'test@gmail.com',
		'capital letters': 'test@GmAil.com',
		'white spaces': '  test@gmail.com     ',
		# 'dots at the end': 'test@gmail.com....',
	}
	User = get_user_model()

	def test_url_exists_at_correct_location(self, options_response):
		assert options_response.status_code == 200

	def test_data_can_be_posted(self, options_response):
		assert 'POST' in options_response.json().get('actions')

	def test_view_accepts_all_the_user_data(self, options_response):
		data = options_response.json()
		for field in self.user_data:
			assert field in data.get('actions').get('POST')

	@pytest.mark.django_db
	def test_registration_impossible_without_full_user_data(self, client):
		"""
		Consecutive requests sent with one field missing.
		"""
		for field in self.user_data:
			data = {item: self.user_data[item] for item in self.user_data if item != field}
			response = client.post(self.register_url, data)
			assert response.status_code == 400

	@pytest.mark.django_db
	def test_registration_impossible_with_invalid_password(self, client):
		f"""
		Invalid passwords are: {list(self.invalid_passwords)}
		"""
		users_before = self.User.objects.all().count()
		for (info, password) in self.invalid_passwords.items():
			data = self.user_data.copy()
			data.update({'password': password, "password_confirm": password})
			response = client.post(self.register_url, data)
			assert response.status_code == 400
			assert 'password' in response.json()
			users_after = self.User.objects.all().count()
			assert users_after - users_before == 0

	@pytest.mark.django_db
	def test_registration_impossible_with_not_matching_passwords(self, client):
		users_before = self.User.objects.all().count()
		data = self.user_data.copy()
		data.update({"password_confirm": f"{data.get('password')}1"})
		response = client.post(self.register_url, data)
		assert response.status_code == 400
		assert 'password_confirm' in response.json()
		users_after = self.User.objects.all().count()
		assert users_after - users_before == 0

	@pytest.mark.django_db
	def test_registration_impossible_with_invalid_email(self, client):
		f"""
		Invalid emails are: {list(self.invalid_emails)}
		"""
		users_before = self.User.objects.all().count()
		for (info, email) in self.invalid_emails.items():
			data = self.user_data.copy()
			data.update({"email": email})
			response = client.post(self.register_url, data)
			assert response.status_code == 400
			assert 'email' in response.json()
			users_after = self.User.objects.all().count()
			assert users_after - users_before == 0

	@pytest.mark.django_db
	def test_registration_impossible_with_too_short_inputs(self, client):
		f"""
		Minimum length for inputs are: {self.input_lengths}
		"""
		users_before = self.User.objects.all().count()
		for (field, length) in self.input_lengths.items():
			data = self.user_data.copy()
			data.update({field: "a" * (length - 1)})
			response = client.post(self.register_url, data)
			assert response.status_code == 400
			assert field in response.json()
			users_after = self.User.objects.all().count()
			assert users_after - users_before == 0

	@pytest.mark.django_db
	def test_user_can_register(self, client):
		users_before = self.User.objects.all().count()
		response = client.post(self.register_url, self.user_data)
		assert response.status_code == 201
		users_after = self.User.objects.all().count()
		assert users_after - users_before == 1

	@pytest.mark.django_db
	def test_user_can_register(self, client):
		"""
		Different emails should be considered as the same one.
		"""
		# TODO: check where the other normalization occurs (serializer?)
		normalized = self.emails['normalized']
		for (info, email) in self.emails.items():
			users_before = self.User.objects.all().count()
			data = self.user_data.copy()
			data.update({'username': info.replace(" ", ""), 'email': email})
			response = client.post(self.register_url, data)
			assert response.status_code == 201
			users_after = self.User.objects.all().count()
			assert users_after - users_before == 1
			assert response.json().get("email") == normalized

	@pytest.mark.django_db
	def test_correct_data_is_returned_after_registration(self, client):
		users_before = self.User.objects.all().count()
		response = client.post(self.register_url, self.user_data)
		assert response.status_code == 201
		users_after = self.User.objects.all().count()
		assert users_after - users_before == 1
		resp_data = response.json()
		user_data = self.user_data
		for field in ['email', 'username', 'first_name', 'last_name']:
			assert resp_data[field] == user_data[field]





