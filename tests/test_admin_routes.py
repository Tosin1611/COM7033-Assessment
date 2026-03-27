import os
import tempfile
import unittest
from app import create_app
from db.sqlite_auth import init_auth_db, create_user, get_user_by_username


class TestAdminRoutes(unittest.TestCase):
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
        create_user(self.db_path, "adminuser", "password123", "admin")
        create_user(self.db_path, "patientuser", "password123", "patient", "P001")

        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def login_as_admin(self):
        return self.client.post("/login", data={
            "username": "adminuser",
            "password": "password123"
        }, follow_redirects=True)

    def login_as_patient(self):
        return self.client.post("/login", data={
            "username": "patientuser",
            "password": "password123"
        }, follow_redirects=True)

    def test_admin_dashboard_requires_login(self):
        response = self.client.get("/admin/dashboard", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please log in first.", response.data)

    def test_patient_cannot_access_admin_dashboard(self):
        self.login_as_patient()
        response = self.client.get("/admin/dashboard", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You are not authorised to access this page.", response.data)

    def test_admin_can_access_dashboard(self):
        self.login_as_admin()
        response = self.client.get("/admin/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Admin Dashboard", response.data)

    def test_admin_can_create_clinician_user(self):
        self.login_as_admin()

        response = self.client.post("/admin/dashboard", data={
            "username": "newclinician",
            "password": "newpass123",
            "role": "clinician",
            "linked_patient_id": ""
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User created successfully.", response.data)

        created_user = get_user_by_username(self.db_path, "newclinician")
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user["role"], "clinician")

    def test_admin_can_create_patient_user_with_linked_patient_id(self):
        self.login_as_admin()

        response = self.client.post("/admin/dashboard", data={
            "username": "newpatient",
            "password": "newpass123",
            "role": "patient",
            "linked_patient_id": "P010"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User created successfully.", response.data)

        created_user = get_user_by_username(self.db_path, "newpatient")
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user["role"], "patient")
        self.assertEqual(created_user["linked_patient_id"], "P010")

    def test_patient_user_creation_requires_linked_patient_id(self):
        self.login_as_admin()

        response = self.client.post("/admin/dashboard", data={
            "username": "badpatient",
            "password": "newpass123",
            "role": "patient",
            "linked_patient_id": ""
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Patient accounts require a valid linked patient ID.", response.data)

        created_user = get_user_by_username(self.db_path, "badpatient")
        self.assertIsNone(created_user)

    def test_duplicate_username_is_rejected(self):
        self.login_as_admin()

        response = self.client.post("/admin/dashboard", data={
            "username": "patientuser",
            "password": "newpass123",
            "role": "patient",
            "linked_patient_id": "P001"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Username already exists.", response.data)

    def test_admin_can_toggle_user_status(self):
        self.login_as_admin()

        user_before = get_user_by_username(self.db_path, "patientuser")
        self.assertEqual(user_before["active"], 1)

        response = self.client.post(f"/admin/toggle_user/{user_before['id']}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User account status updated.", response.data)

        user_after = get_user_by_username(self.db_path, "patientuser")
        self.assertEqual(user_after["active"], 0)


if __name__ == "__main__":
    unittest.main()