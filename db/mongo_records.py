from pymongo import MongoClient

mongo_client = None
records_collection = None


def init_mongo_records(uri, db_name, collection_name):
    global mongo_client, records_collection

    mongo_client = MongoClient(uri)
    db = mongo_client[db_name]
    records_collection = db[collection_name]

    if records_collection.count_documents({}) == 0:
        seed_default_patient_records()


def seed_default_patient_records():
    records_collection.insert_many([
        {
            "patient_id": "P001",
            "full_name": "Alice Johnson",
            "age": 42,
            "sex": "Female",
            "blood_pressure": "130/85",
            "cholesterol": "205",
            "resting_ecg": "Normal",
            "medical_history": "Hypertension",
            "appointments": [
                {"date": "2026-03-20", "details": "Routine cardiac review"}
            ],
            "prescriptions": [
                {"date": "2026-03-10", "drug": "Lisinopril", "dosage": "10mg daily"}
            ],
            "consultation_notes": [
                {"date": "2026-03-10", "clinician": "clinician1", "note": "Stable blood pressure."}
            ]
        }
    ])


def get_patient_record(patient_id):
    return records_collection.find_one({"patient_id": patient_id}, {"_id": 0})