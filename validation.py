import re
from telegram.ext import MessageHandler, filters
import User.user as user

NAME_PATTERN = r'^[А-ЯЁа-яёA-Za-z-]{2,30}$'

AGE_PATTERN = r'^(1[0-2]0|[1-9][0-9]?)$'

CITY_PATTERN = r'^[А-ЯЁа-яёA-Za-z\s-]{2,50}$'


def validate_name(name: str) -> bool:
    return bool(re.fullmatch(NAME_PATTERN, name.strip()))

def validate_age(age: str) -> bool:
    return bool(re.fullmatch(AGE_PATTERN, age.strip()))

def validate_city(city: str) -> bool:
    return bool(re.fullmatch(CITY_PATTERN, city.strip()))