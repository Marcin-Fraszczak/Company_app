from rest_registration.exceptions import BadRequest


class NoFirstName(BadRequest):
	default_detail = {"first_name": "First name must be set"}


class NoLastName(BadRequest):
	default_detail = {"last_name": "Last name must be set"}
