# Secure Healthcare Management Flask Application

## Overview

This project is a secure healthcare management web application developed with Flask.  
It was designed for the Secure Software Development module and follows the Secure Software Development Life Cycle (SSDLC) approach.

The system supports three user roles:

- Patient
- Clinician
- Admin

The application allows authorised users to securely access and manage healthcare information while applying secure design principles taught in the module.

---

## Purpose of the System

The purpose of this system is to provide a web-based healthcare record management platform that supports:

- secure login for registered users
- role-based access control
- patient access to their own healthcare records
- clinician access to patient records for treatment and monitoring
- administrator control of user accounts and role management
- accountability through logging of security-relevant actions

The system was designed to support confidentiality, integrity, availability, and accountability when handling sensitive healthcare data.

---

## Main Features

### Authentication
- login using username and password
- password hashing using Werkzeug
- session-based access control
- logout functionality

### Patient Features
- view own profile
- view own appointments
- view own prescriptions
- view own consultation notes and medical summary

### Clinician Features
- search patient records
- view patient records
- update patient details
- add consultation notes
- add prescriptions
- add appointments

### Admin Features
- create user accounts
- assign roles
- link patient accounts to patient IDs
- activate or deactivate user accounts

---

## Security Features Implemented

The application includes the following secure programming measures based on the lecture materials:

- password hashing before storage
- role-based access control enforced on the server side
- session-based authentication
- input validation on submitted data
- separation of authentication data and healthcare data
- logging of security-relevant events
- protection of patient data through role and ownership checks

### Security Design Decisions
- SQLite is used for authentication and account data
- MongoDB is used for patient healthcare records
- passwords are never stored in plaintext
- patients can only access their own record
- clinicians can search and update patient records
- administrative actions are restricted to admin users only

---

## Technologies Used

- Python
- Flask
- SQLite
- MongoDB
- PyMongo
- Werkzeug Security
- HTML Templates
- Python Logging
- unittest

---

## Project Structure

```text
your_project/
│
├── app.py
├── config.py
├── validators.py
├── auth_helpers.py
├── requirements.txt
├── README.md
├── app.log
│
├── db/
│   ├── sqlite_auth.py
│   └── mongo_records.py
│
├── routes/
│   ├── auth_routes.py
│   ├── patient_routes.py
│   ├── clinician_routes.py
│   └── admin_routes.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── patient_dashboard.html
│   ├── clinician_dashboard.html
│   ├── clinician_patient.html
│   └── admin_dashboard.html
│
└── tests/
    ├── test_validators.py
    ├── test_auth_routes.py
    └── test_access_control.py