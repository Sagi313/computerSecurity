import json
import re

from django.utils.translation import gettext as _
from django.core.exceptions import FieldError, ValidationError
from webApp.models import PasswordsHistory
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

with open("webApp/config/pass.json") as file:
    rules = json.load(file)


class AuthHelper:
    def __init__(self):
        self.rules = rules

    def validate(self, password, user=None):
        is_valid_register(user)
        validate_pass(password, user)
 

        
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


def validate_pass(password, user):
    if len(password) < rules['len']:
        raise ValidationError(f"password must contain at least {rules['len']} characters", code='invalid')
    elif not all(re.search(i, password) for i in rules["must_include"]):
        raise ValidationError(f"password must include: {make_prettier_condition('must_include')} ", code='invalid')
    elif password in rules["dict_pass"]:
        raise ValidationError("common passwords are not allowed", code='invalid')
    elif not check_pass_history(password, user):
        raise ValidationError(f'New password must be different from the last {rules["history"]} password',
                              code='invalid')
    save_old_password(password, user)


def check_pass_history(password, user):
    pass_list = PasswordsHistory.objects.filter(user=user.username).order_by('-id')[:rules['history']][::-1]
    for i in pass_list:
        old_pass = i.pwd
        if check_password(password,old_pass):
            return False
    return True


def save_old_password(password, user):
    PasswordsHistory.objects.get_or_create(user=user.username,
                                           pwd=make_password(password))

def is_valid_register(user):
    if user.username in [user.username for user in User.objects.all()]:
        raise ValidationError(f"User is already been taken", code='invalid')
    if not user.first_name.isalpha():
        raise ValidationError(f"First name not valid", code='invalid')
    if not user.last_name.isalpha():
        raise ValidationError(f"Last name not valid", code='invalid')
    if not (user.email.find('@') and user.email.find('.')):
        if not user.email.find('@') < user.email.find('.'):
            raise ValidationError(f"Email not valid", code='invalid')
    if user.email in [user.email for user in User.objects.all()]:
        raise ValidationError(f"Email is already been used", code='invalid')