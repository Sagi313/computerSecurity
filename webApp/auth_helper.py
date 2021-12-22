import json
import re
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


class AuthHelper:
    def __init__(self):
        with open("config/pass.json") as file:
            rules = json.load(file)
        self.rules = rules

    def validate(self, password, user=None):

        if len(password) < self.rules['len']:
            raise ValidationError(
                _(f"This password must contain at least {self.rules['len']} characters."),
                code='password_too_short',
                params={'min_length': self.rules['len']},
            )

        elif not all(re.search(i, password) for i in self.rules["has_to_Include"]):
            raise ValidationError(
                _(f"This password must contain all of the next:  {self.rules['has_to_Include']} characters."),
                code='not all off the chars',
                params={'must Include': self.rules["has_to_Include"]},
            )
        elif password in self.rules["dict_pass"]:
            raise ValidationError(
                _(f"This password {self.rules['has_to_Include']} is not allowed."),
                code='dict pass',
                params={'must Include': self.rules["has_to_Include"]},
            )

    def get_help_text(self):
        error_str = f"min len : {self.rules['len']} \n Must include: {self.rules['has_to_Include']}"
        return _(f"min len : {self.rules['len']},  \n "
                 f"Must include: {self.rules['has_to_Include']}")
