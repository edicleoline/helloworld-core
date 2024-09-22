from __future__ import annotations

import phonenumbers
import re

def is_valid_phone(phone: str, region: str = "BR") -> bool:
    try:
        parsed_phone = phonenumbers.parse(phone, region)
        return phonenumbers.is_valid_number(parsed_phone)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

def is_valid_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))