import re
from datetime import datetime


def validate_patient_id(patient_id):
    if not patient_id:
        return False, "Patient ID is required."
    if not re.fullmatch(r"[A-Za-z0-9_-]+", patient_id.strip()):
        return False, "Invalid patient ID format."
    return True, ""


def validate_name(name):
    if not name:
        return False, "Name is required."
    name = name.strip()
    if len(name) < 2 or len(name) > 100:
        return False, "Name must be between 2 and 100 characters."
    if not re.fullmatch(r"[A-Za-z .'-]+", name):
        return False, "Invalid name format."
    return True, ""


def validate_age(age):
    try:
        age_value = int(age)
        if age_value < 0 or age_value > 120:
            return False, "Age must be between 0 and 120."
        return True, ""
    except (ValueError, TypeError):
        return False, "Age must be a number."


def validate_text_field(value, field_name, min_length=1, max_length=500):
    if not value:
        return False, f"{field_name} is required."
    value = value.strip()
    if len(value) < min_length or len(value) > max_length:
        return False, f"{field_name} must be between {min_length} and {max_length} characters."
    return True, ""


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True, ""
    except (ValueError, TypeError):
        return False, "Date must be in YYYY-MM-DD format."
    
def validate_username(username):
    if not username:
        return False, "Username is required."
    username = username.strip()
    if len(username) < 3 or len(username) > 30:
        return False, "Username must be between 3 and 30 characters."
    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        return False, "Username can contain only letters, numbers and underscores."
    return True, ""


def validate_password(password):
    if not password:
        return False, "Password is required."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    return True, ""


def validate_role(role):
    allowed_roles = ["patient", "clinician", "admin"]
    if role not in allowed_roles:
        return False, "Invalid role."
    return True, ""