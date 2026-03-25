import os
import tempfile
import unittest
from app import create_app
from db.sqlite_auth import init_auth_db, create_user


class TestAccessControl(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

        self.app = create_app({
            "TESTING": True,
            "SECRET_KEY": "test_secret",
            "AUTH_DB_PATH": self.db_path,
            "MONGO_URI": "mongodb://localhost:27017/",
            "MONGO_DB_NAME": "test_secure_healthcare",
            "MONGO_COLLECTION": "test_patient_records"
        })

        init_auth_db(self.db_path)
        create_user(self.db_path, "patientuser", "password123", "patient", "P001")
        create_user(self.db_path, "clinicianuser", "password123", "clinician")
        create_user(self.db_path, "adminuser", "password123", "admin")

        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_patient_cannot_access_admin_dashboard(self):
        self.client.post("/login", data={
            "username": "patientuser",
            "password": "password123"
        }, follow_redirects=True)

        response = self.client.get("/admin/dashboard", follow_redirects=True)
        self.assertIn(b"You are not authorised to access this page.", response.data)

    def test_admin_can_access_admin_dashboard(self):
        self.client.post("/login", data={
            "username": "adminuser",
            "password": "password123"
        }, follow_redirects=True)

        response = self.client.get("/admin/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Admin Dashboard", response.data)

    def test_clinician_can_access_clinician_dashboard(self):
        self.client.post("/login", data={
            "username": "clinicianuser",
            "password": "password123"
        }, follow_redirects=True)

        response = self.client.get("/clinician/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Clinician Dashboard", response.data)


if __name__ == "__main__":
    unittest.main()