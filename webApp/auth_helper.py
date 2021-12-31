import json
import re
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

with open("webApp/config/pass.json") as file:
    rules = json.load(file)


class AuthHelper:
    def __init__(self):
        self.rules = rules

    def validate(self, password, user=None):
        validate_pass(password)

    def get_help_text(self):
        must_include = make_prettier_condition("must_include")
        return _(f"Minimum len : {self.rules['len']},  \n "
                 f"Must include: {must_include}")


def make_prettier_condition(conditions):
    tmp_str = ""
    for condition in rules[conditions]:
        tmp_str = tmp_str + f"{condition}  ,"
    return replace_char(tmp_str)


def replace_char(string_value: str):
    string_value = string_value.replace('[', ' ')
    string_value = string_value.replace(']', ' ')
    string_value = string_value[:-1]
    return string_value


def validate_pass(password):
    if len(password) < rules['len']:
        raise ValidationError(f"password must contain at least {rules['len']} characters", code='invalid')
    elif not all(re.search(i, password) for i in rules["must_include"]):
        raise ValidationError(f"password must include: {make_prettier_condition('must_include')} ", code='invalid')
    elif password in rules["dict_pass"]:
        raise ValidationError("common passwords are not allowed", code='invalid')
