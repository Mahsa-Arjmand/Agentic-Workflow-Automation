import sqlite3
from pathlib import Path
from config import DATA_DIR

DB_PATH = DATA_DIR / "hospital_assist.db"


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                icon TEXT
            );

            CREATE TABLE IF NOT EXISTS functionalities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER,
                code TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                keywords TEXT,
                steps TEXT,
                access_path TEXT,
                usage_count INTEGER DEFAULT 0,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            );

            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                functionality_id INTEGER,
                customer_query TEXT,
                matched_score REAL,
                was_successful INTEGER DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (functionality_id) REFERENCES functionalities(id)
            );
        """)


def seed_data():
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM functionalities").fetchone()[0]
        if count > 0:
            return

    categories = [
        (1, "Appointments", "Schedule, cancel, or reschedule appointments"),
        (2, "Medical Records", "Access test results, prescriptions, and medical history"),
        (3, "Billing & Insurance", "Payments, insurance claims, and billing inquiries"),
        (4, "Emergency Services", "Emergency room, ambulance, and urgent care"),
        (5, "Pharmacy", "Prescriptions, refills, and medication inquiries"),
        (6, "Inpatient Services", "Admission, discharge, room services"),
        (7, "Specialist Referrals", "Referrals to specialists and consultations"),
    ]

    functionalities = [
        (1, "APT-001", "Schedule Appointment",
         "Book a new appointment with a doctor or specialist.",
         "appointment, book, schedule, visit, doctor, new, make appointment, see doctor, need doctor",
         "1. Ask which department (General, Cardiology, Orthopedics, Neurology, etc.)\n2. Check available time slots\n3. Next available: Dr. Ahmadi (General), Monday 10:00 AM\n4. Get patient national ID and insurance info\n5. Book appointment and send SMS confirmation\n6. Remind to arrive 15 minutes early with ID and insurance card",
         "Main Menu > Appointments > Schedule New"),

        (1, "APT-002", "Cancel Appointment",
         "Cancel an existing appointment.",
         "cancel, appointment, can't make it, cancel visit, remove",
         "1. Get appointment reference number or patient ID\n2. Verify patient identity\n3. Confirm cancellation - no charge if 24+ hours before\n4. Cancel in system\n5. Offer to reschedule for another date\n6. Send cancellation SMS confirmation",
         "Main Menu > Appointments > Cancel"),

        (1, "APT-003", "Reschedule Appointment",
         "Change date or time of an existing appointment.",
         "reschedule, change time, move appointment, different day, change date",
         "1. Get original appointment reference number\n2. Verify patient identity\n3. Show available slots in same department\n4. Book new slot: Wednesday 2:00 PM available\n5. Old appointment automatically cancelled\n6. Send new confirmation SMS with updated details",
         "Main Menu > Appointments > Reschedule"),

        (1, "APT-004", "Walk-in Registration",
         "Register for same-day walk-in visit without appointment.",
         "walk in, today, same day, urgent, now, without appointment, immediate",
         "1. Check walk-in availability (current wait time: 45 minutes)\n2. Register patient details (name, national ID, insurance)\n3. Assign queue number: W-042\n4. Direct patient to waiting area\n5. Notify when doctor is ready via display screen\n6. Estimated consultation time: 15-20 minutes",
         "Main Menu > Appointments > Walk-in"),

        (2, "MED-001", "Test Results Inquiry",
         "Access and explain laboratory test results.",
         "test, results, lab, blood, xray, MRI, CT scan, report, my results, lab results",
         "1. Verify patient identity with national ID\n2. Ask which test (Blood work, X-ray, MRI, CT scan, etc.)\n3. Retrieve results from system\n4. Blood test: All values within normal range ✅\n5. Explain results in simple, clear terms\n6. Email PDF report if requested\n7. Note if doctor follow-up is needed",
         "Main Menu > Medical Records > Test Results"),

        (2, "MED-002", "Prescription Reprint",
         "Request a copy of a previous or lost prescription.",
         "prescription, copy, lost, reprint, medication list, drug list, need prescription",
         "1. Verify patient identity with national ID\n2. Check last prescription date: 1404/05/20\n3. Medications prescribed: Metformin 500mg (2x daily), Losartan 50mg (1x daily)\n4. Print physical copy or email PDF version\n5. Note: Prescription valid for 30 days from issue date\n6. Advise if medication renewal consultation is needed",
         "Main Menu > Medical Records > Prescriptions"),

        (2, "MED-003", "Medical History Access",
         "View patient's complete medical history.",
         "history, medical history, previous, record, past, conditions, allergies, what conditions",
         "1. Verify patient identity with national ID\n2. Retrieve complete medical history from database\n3. Chronic conditions: Diabetes Type 2, Hypertension\n4. Allergies: Penicillin (severe reaction)\n5. Previous surgeries: Appendectomy (1398)\n6. Current medications: Metformin, Losartan\n7. Share summary with patient (print or email)",
         "Main Menu > Medical Records > History"),

        (2, "MED-004", "Doctor's Note Request",
         "Request a sick note or medical certificate for work/school.",
         "note, sick note, doctor note, work, school, excuse, certificate, medical certificate",
         "1. Verify patient identity\n2. Check last visit date: 2 days ago with Dr. Rezaei\n3. Generate standard medical certificate\n4. Rest period: 1404/06/12 to 1404/06/15 (3 days)\n5. Doctor's signature required - sent to doctor's queue\n6. Available for pickup in 2 hours or sent via email\n7. Cost: Free (included in consultation)",
         "Main Menu > Medical Records > Doctor's Note"),

        (3, "BIL-001", "Bill Payment",
         "Pay hospital bills and view detailed billing breakdown.",
         "bill, payment, pay, invoice, charge, cost, how much, pay bill, billing",
         "1. Verify patient identity\n2. Outstanding balance: 2,450,000 Toman\n3. Breakdown: Consultation (350K) + Lab tests (800K) + Medications (1,300K)\n4. Due date: 1404/06/20\n5. Payment options: Online payment, Card (in-person), Cash, Installments\n6. Process payment securely\n7. Send payment receipt via SMS and email",
         "Main Menu > Billing > Pay Bill"),

        (3, "BIL-002", "Insurance Verification",
         "Check insurance coverage, benefits, and co-pay amounts.",
         "insurance, coverage, covered, Tamin, Salamat, complementary, what does insurance cover, my insurance",
         "1. Ask for insurance type (Tamin Ejtemaei, Salamat, Kosar, etc.)\n2. Verify insurance card number and expiry date\n3. Coverage details: Tamin covers 90% inpatient, 70% outpatient\n4. Patient co-pay: 10-30% depending on service type\n5. Check if specific procedure/medication is covered\n6. Pre-authorization may be needed for surgeries\n7. Provide coverage summary to patient",
         "Main Menu > Billing > Insurance Check"),

        (3, "BIL-003", "Insurance Claim Submission",
         "Submit insurance claim for reimbursement.",
         "claim, insurance claim, reimbursement, submit, paperwork, insurance form, get money back",
         "1. Verify insurance details and policy number\n2. Get treatment dates and total costs\n3. Required documents: Doctor's note, receipts, claim form\n4. Submit claim to insurance company electronically\n5. Processing time: 2-4 weeks for review\n6. Track claim status with reference: CLM-14040612-001\n7. Reimbursement sent to registered bank account",
         "Main Menu > Billing > Submit Claim"),

        (3, "BIL-004", "Payment Plan Request",
         "Set up installment payment plan for large medical bills.",
         "installment, payment plan, can't pay, too expensive, monthly, split, broke",
         "1. Verify patient identity\n2. Total bill amount: 5,000,000 Toman\n3. Available plans: 3 months (1.7M/mo), 6 months (850K/mo), 12 months (450K/mo)\n4. No interest for plans up to 6 months\n5. Set up automatic monthly debit from bank account\n6. First payment due in 30 days\n7. Sign payment plan agreement digitally",
         "Main Menu > Billing > Payment Plan"),

        (4, "EMG-001", "Emergency Room Guide",
         "Guide patients to emergency room and explain triage process.",
         "emergency, ER, urgent, accident, pain, bleeding, ambulance, 911, emergency room",
         "1. Assess urgency level: Red (immediate), Yellow (30 min), Green (2 hours)\n2. Current ER wait times displayed on board\n3. Direct to ER entrance: Ground floor, West wing\n4. What to bring: National ID, insurance card\n5. Triage nurse will assess condition on arrival\n6. Emergency contact: 115 for ambulance dispatch\n7. Translator available if needed",
         "Main Menu > Emergency > ER Guide"),

        (4, "EMG-002", "Ambulance Request",
         "Request ambulance dispatch for emergency transport.",
         "ambulance, dispatch, pick up, transport, emergency transport, need ambulance",
         "1. Confirm exact location and patient condition\n2. Dispatch nearest available ambulance\n3. Estimated arrival time: 15 minutes\n4. Ambulance ID: AMB-042 (track via app)\n5. Cost: 500,000 Toman (partially covered by insurance)\n6. Instructions: Stay calm, prepare ID and insurance card\n7. Track ambulance location in real-time",
         "Main Menu > Emergency > Ambulance"),

        (5, "PHA-001", "Prescription Refill",
         "Refill an existing prescription medication.",
         "refill, prescription, medicine, medication, renew, running out, need more, out of medicine",
         "1. Verify patient identity with national ID\n2. Check current prescription: Metformin 500mg, prescribed 1404/05/20\n3. Refills remaining: 2\n4. Process refill request - ready in 1 hour\n5. Cost: 85,000 Toman (after insurance discount)\n6. Pickup location: Hospital Pharmacy, Ground floor\n7. Notify patient when ready via SMS",
         "Main Menu > Pharmacy > Refill"),

        (5, "PHA-002", "Medication Information",
         "Get detailed information about medications, side effects, and interactions.",
         "medicine, medication, side effects, dosage, how to take, interaction, drug info, what does this do",
         "1. Ask for medication name\n2. Look up: Metformin 500mg\n3. Usage: Take with meals, twice daily (morning and evening)\n4. Common side effects: Nausea, stomach upset (usually temporary)\n5. Serious side effects: Lactic acidosis (rare but seek immediate help)\n6. Drug interactions: Avoid alcohol, certain contrast dyes\n7. Warning: Do not stop taking without consulting your doctor",
         "Main Menu > Pharmacy > Drug Info"),

        (5, "PHA-003", "OTC Medication Recommendation",
         "Recommend over-the-counter medications for common ailments.",
         "OTC, over counter, without prescription, cold, headache, pain, allergy, fever, cough",
         "1. Ask about symptoms and duration\n2. For headache/mild pain: Acetaminophen 500mg every 6 hours\n3. For cold/flu: Cold relief tablets + Vitamin C supplements\n4. For allergies: Cetirizine 10mg once daily\n5. Available at hospital pharmacy without prescription\n6. Cost range: 25,000 - 85,000 Toman\n7. Warning: See doctor if symptoms persist beyond 3 days",
         "Main Menu > Pharmacy > OTC"),

        (6, "INP-001", "Admission Process",
         "Guide through hospital admission and room assignment.",
         "admission, admitted, stay, inpatient, check in, hospitalized, staying overnight",
         "1. Verify doctor's admission order in system\n2. Get patient personal details and insurance information\n3. Room options: General Ward (2-bed, 500K/day), Private (1-bed, 1.5M/day)\n4. Required deposit: 3 days advance payment\n5. Assign room: Room 302, Bed A\n6. Provide: Hospital gown, meal schedule, visiting hours info\n7. Visiting hours: 4:00 PM - 8:00 PM (max 2 visitors)",
         "Main Menu > Inpatient > Admission"),

        (6, "INP-002", "Discharge Process",
         "Handle patient discharge from hospital.",
         "discharge, leave, going home, release, check out, leaving hospital",
         "1. Verify doctor's discharge order is signed\n2. Prepare discharge summary with treatment details\n3. Final bill calculation: 4,500,000 Toman (3 days stay)\n4. Insurance adjustment: -3,600,000 Toman\n5. Patient responsibility: 900,000 Toman\n6. Provide: Discharge papers, new prescriptions, follow-up appointment date\n7. Arrange wheelchair/transportation if needed",
         "Main Menu > Inpatient > Discharge"),

        (6, "INP-003", "Room Service Request",
         "Request food, maintenance, or additional amenities.",
         "room, food, meal, maintenance, broken, TV, bathroom, clean, pillow, blanket",
         "1. Ask request type: Food/Maintenance/Amenities\n2. Food: Menu available, next meal served at 12:30 PM\n3. Special diet options: Diabetic, Low-salt, Vegetarian available\n4. Maintenance issue: Technician dispatched within 30 minutes\n5. Extra items (pillow/blanket): Delivered within 15 minutes\n6. TV not working? Contact internal extension 500\n7. Visitor policy reminder: 2 visitors max, 4-8 PM",
         "Main Menu > Inpatient > Room Service"),

        (7, "REF-001", "Specialist Referral",
         "Get referral to a specialist doctor from GP.",
         "referral, specialist, cardiologist, neurologist, orthopedist, refer, see specialist, heart doctor",
         "1. Get reason for referral from General Practitioner\n2. Check available specialists in requested field\n3. Cardiologist: Dr. Mohammadi, next available Thursday 9:00 AM\n4. Neurologist: Dr. Hosseini, next available Monday 11:00 AM\n5. Process referral and book specialist appointment\n6. Send referral letter to specialist's office\n7. Send appointment confirmation SMS to patient",
         "Main Menu > Referrals > New Referral"),

        (7, "REF-002", "Second Opinion Request",
         "Request a second opinion from another doctor.",
         "second opinion, another doctor, different doctor, consult, opinion, not sure",
         "1. Get current diagnosis and treatment plan details\n2. Find alternative specialist in the same field\n3. Dr. Karimi available for second opinion consultation\n4. Send medical records securely to Dr. Karimi\n5. Book consultation: Friday 2:00 PM\n6. Cost: 850,000 Toman (may be partially covered by insurance)\n7. Second opinion report available within 48 hours after consultation",
         "Main Menu > Referrals > Second Opinion"),
    ]

    with get_connection() as conn:
        for cat in categories:
            conn.execute("INSERT INTO categories (id, name, description, icon) VALUES (?, ?, ?, ?)", cat)
        for func in functionalities:
            conn.execute(
                "INSERT INTO functionalities (category_id, code, title, description, keywords, steps, access_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
                func
            )
        conn.commit()


def get_all_functionalities():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT f.*, c.name as category_name, c.icon as category_icon
            FROM functionalities f
            LEFT JOIN categories c ON f.category_id = c.id
            ORDER BY f.usage_count DESC, f.title
        """).fetchall()
        return [dict(row) for row in rows]


def get_functionality_by_code(code: str):
    with get_connection() as conn:
        row = conn.execute("""
            SELECT f.*, c.name as category_name, c.icon as category_icon
            FROM functionalities f
            LEFT JOIN categories c ON f.category_id = c.id
            WHERE f.code = ?
        """, (code,)).fetchone()
        return dict(row) if row else None


def get_categories():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM categories ORDER BY name").fetchall()
        return [dict(row) for row in rows]


def increment_usage(code: str):
    with get_connection() as conn:
        conn.execute("UPDATE functionalities SET usage_count = usage_count + 1 WHERE code = ?", (code,))
        conn.commit()


def log_usage(functionality_code: str, customer_query: str, was_successful: int = 1):
    with get_connection() as conn:
        func = get_functionality_by_code(functionality_code)
        if func:
            conn.execute(
                "INSERT INTO usage_logs (functionality_id, customer_query, matched_score, was_successful) VALUES (?, ?, 1.0, ?)",
                (func['id'], customer_query, was_successful)
            )
            conn.commit()