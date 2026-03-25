import unittest
from validators import validate_username, validate_password, validate_role, validate_patient_id, validate_age, validate_date


class TestValidators(unittest.TestCase):
    def test_validate_username_valid(self):
        valid, _ = validate_username("patient_1")
        self.assertTrue(valid)

    def test_validate_username_invalid(self):
        valid, _ = validate_username("bad username!")
        self.assertFalse(valid)

    def test_validate_password_valid(self):
        valid, _ = validate_password("password123")
        self.assertTrue(valid)

    def test_validate_password_invalid(self):
        valid, _ = validate_password("short")
        self.assertFalse(valid)

    def test_validate_role(self):
        valid, _ = validate_role("admin")
        self.assertTrue(valid)

        valid, _ = validate_role("manager")
        self.assertFalse(valid)

    def test_validate_patient_id(self):
        valid, _ = validate_patient_id("P001")
        self.assertTrue(valid)

    def test_validate_age(self):
        valid, _ = validate_age("45")
        self.assertTrue(valid)

        valid, _ = validate_age("200")
        self.assertFalse(valid)

    def test_validate_date(self):
        valid, _ = validate_date("2026-03-20")
        self.assertTrue(valid)

        valid, _ = validate_date("20/03/2026")
        self.assertFalse(valid)


if __name__ == "__main__":
    unittest.main()