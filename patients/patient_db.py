"""
MedAssist - Patient Database Management
SQLite database for patient profiles, allergies, and medical history
"""

import os
import sqlite3
import hashlib
import json
import re
from datetime import datetime
from typing import Optional, List, Dict, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "patients.db")


class PatientDatabase:
    """SQLite database for patient management"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path if db_path else DEFAULT_DB_PATH
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with all tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                phone_number TEXT,
                blood_type TEXT,
                height_cm REAL,
                weight_kg REAL,
                emergency_contact_name TEXT,
                emergency_contact_phone TEXT,
                doctor_name TEXT,
                doctor_phone TEXT,
                language_preference TEXT DEFAULT 'English',
                village TEXT,
                district TEXT,
                state TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Allergies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS allergies (
                allergy_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                medicine_name TEXT NOT NULL,
                generic_name TEXT,
                severity TEXT,  -- Mild, Moderate, Severe
                symptoms TEXT,
                reaction_date TIMESTAMP,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
            )
        ''')
        
        # Medical history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                disease_name TEXT NOT NULL,
                diagnosis_date TIMESTAMP,
                severity TEXT,
                symptoms TEXT,
                treatment_given TEXT,
                doctor_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
            )
        ''')
        
        # Medical reports
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_reports (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                disease_diagnosed TEXT,
                symptoms_reported TEXT,
                tests_recommended TEXT,  -- JSON
                drugs_prescribed TEXT,  -- JSON
                precautions TEXT,
                llm_response TEXT,
                confidence_score REAL,
                doctor_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
            )
        ''')
        
        # Voice interactions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voice_interactions (
                interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                language TEXT,
                user_input_text TEXT,
                system_response_text TEXT,
                interaction_type TEXT,
                duration_seconds INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
            )
        ''')
        
        # Medicine reactions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicine_reactions (
                reaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                medicine_name TEXT NOT NULL,
                reaction_type TEXT DEFAULT 'allergy',
                severity TEXT DEFAULT 'Moderate',
                reaction_description TEXT,
                symptoms TEXT,
                voice_input BOOLEAN DEFAULT 0,
                reported_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patients_username ON patients(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_allergies_patient ON allergies(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_medical_history_patient ON medical_history(patient_id)')
        # Ensure demo patient has persistent registration allergies
        try:
            cursor.execute("SELECT patient_id FROM patients WHERE username = 'demo'")
            demo_row = cursor.fetchone()
            if demo_row:
                demo_pid = demo_row[0]
                cursor.execute("SELECT COUNT(*) FROM allergies WHERE patient_id = ?", (demo_pid,))
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO allergies (patient_id, medicine_name, generic_name, severity, symptoms, notes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (demo_pid, "Aspirin", "Acetylsalicylic acid", "Severe", "Facial swelling, hives, breathing difficulty", "Permanent registration allergy record"))
                    cursor.execute('''
                        INSERT INTO allergies (patient_id, medicine_name, generic_name, severity, symptoms, notes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (demo_pid, "Sulfa antibiotics", "Sulfamethoxazole", "Moderate", "Skin rash, intense itching", "Permanent registration allergy record"))
                    cursor.execute('''
                        INSERT INTO medicine_reactions (patient_id, medicine_name, reaction_type, severity, reaction_description, symptoms, voice_input)
                        VALUES (?, ?, ?, ?, ?, ?, 0)
                    ''', (demo_pid, "Aspirin", "allergy", "Severe", "Facial swelling and hives", '["Facial swelling", "hives"]'))
        except Exception as e:
            print(f"[DB] Demo allergies check notice: {e}")

        conn.commit()
        conn.close()
    
    # ==================== AUTHENTICATION ====================
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password with SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_patient(self, 
                        username: str, 
                        email: str, 
                        password: str,
                        full_name: str,
                        age: int = None,
                        gender: str = None,
                        phone: str = None,
                        blood_type: str = None) -> Tuple[bool, str, Optional[int]]:
        """
        Register new patient
        Returns: (success, message, patient_id)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if username/email exists
            cursor.execute('SELECT patient_id FROM patients WHERE username = ? OR email = ?',
                         (username, email))
            if cursor.fetchone():
                return False, "Username or email already exists!", None
            
            # Insert new patient
            cursor.execute('''
                INSERT INTO patients (
                    username, email, password_hash, full_name, age, gender,
                    phone_number, blood_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                username, email, self.hash_password(password),
                full_name, age, gender, phone, blood_type
            ))
            
            patient_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, "Registration successful!", patient_id
        
        except Exception as e:
            return False, f"Registration failed: {str(e)}", None
    
    def login_patient(self, username: str, password: str) -> Tuple[bool, str, Optional[int]]:
        """
        Login patient
        Returns: (success, message, patient_id)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT patient_id, password_hash FROM patients WHERE username = ?',
                         (username,))
            result = cursor.fetchone()
            
            if not result:
                return False, "Username not found!", None
            
            patient_id, stored_hash = result
            if stored_hash != self.hash_password(password):
                return False, "Incorrect password!", None
            
            conn.close()
            return True, "Login successful!", patient_id
        
        except Exception as e:
            return False, f"Login failed: {str(e)}", None
    
    # ==================== PATIENT PROFILE ====================
    
    def get_patient(self, patient_id: int) -> Optional[Dict]:
        """Get patient profile"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return dict(result)
            return None
        
        except Exception as e:
            print(f"Error fetching patient: {e}")
            return None

    # Convenience alias
    get_patient_by_id = get_patient
    
    def update_patient(self, patient_id: int, **kwargs) -> Tuple[bool, str]:
        """Update patient profile"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            allowed_fields = [
                'full_name', 'age', 'gender', 'phone_number', 'blood_type',
                'height_cm', 'weight_kg', 'emergency_contact_name',
                'emergency_contact_phone', 'doctor_name', 'doctor_phone',
                'language_preference', 'village', 'district', 'state'
            ]
            
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
            
            if not updates:
                return True, "No updates to make"
            
            set_clause = ', '.join([f'{k} = ?' for k in updates.keys()])
            values = list(updates.values()) + [patient_id]
            
            cursor.execute(f'UPDATE patients SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE patient_id = ?',
                         values)
            
            conn.commit()
            conn.close()
            return True, "Profile updated!"
        
        except Exception as e:
            return False, f"Update failed: {str(e)}"
    
    # ==================== ALLERGIES ====================
    
    def add_allergy(self, patient_id: int, medicine_name: str, severity: str,
                   symptoms: str = "", generic_name: str = "", notes: str = "") -> Tuple[bool, str]:
        """Add patient allergy and sync with reactions table"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO allergies (
                    patient_id, medicine_name, generic_name, severity,
                    symptoms, reaction_date, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_id, medicine_name.strip(), generic_name.strip(), severity,
                symptoms, datetime.now(), notes
            ))
            
            # Synchronize into medicine_reactions table if present
            try:
                cursor.execute('''
                    INSERT INTO medicine_reactions (
                        patient_id, medicine_name, reaction_type, severity,
                        reaction_description, symptoms, voice_input
                    ) VALUES (?, ?, ?, ?, ?, ?, 0)
                ''', (
                    patient_id, medicine_name.strip(), 'allergy', severity,
                    notes or f"Reported allergy to {medicine_name}",
                    json.dumps([symptoms]) if symptoms else "[]"
                ))
            except Exception:
                pass

            conn.commit()
            conn.close()
            return True, "Allergy recorded successfully!"
        
        except Exception as e:
            return False, f"Failed to add allergy: {str(e)}"
    
    def delete_allergy(self, patient_id: int, allergy_id: int) -> Tuple[bool, str]:
        """Delete patient allergy by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM allergies WHERE allergy_id = ? AND patient_id = ?',
                           (allergy_id, patient_id))
            conn.commit()
            conn.close()
            return True, "Allergy record removed successfully!"
        except Exception as e:
            return False, f"Failed to remove allergy: {str(e)}"

    def get_allergies(self, patient_id: int) -> List[Dict]:
        """Get all allergies for patient"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM allergies WHERE patient_id = ? ORDER BY reaction_date DESC', (patient_id,))
            results = cursor.fetchall()
            conn.close()
            
            return [dict(r) for r in results]
        
        except Exception as e:
            print(f"Error fetching allergies: {e}")
            return []
    
    def check_drug_allergy(self, patient_id: int, drug_name: str) -> Tuple[bool, Optional[Dict]]:
        """
        Check if patient is allergic to a drug, with fuzzy, bidirectional and token overlap checking.
        Returns: (is_allergic, allergy_details)
        """
        if not drug_name or not patient_id:
            return False, None

        try:
            allergies = self.get_allergies(patient_id)
            clean_q = re.sub(r'[^a-zA-Z0-9\s]', ' ', drug_name.lower()).strip()
            q_tokens = set(clean_q.split())
            ignore_tokens = {"mg", "ml", "tab", "tablet", "tablets", "syrup", "capsule", "capsules", "injection", "drops", "for", "with", "take", "and"}

            # Check direct allergies list
            for item in allergies:
                med_name = (item.get('medicine_name') or '').lower().strip()
                gen_name = (item.get('generic_name') or '').lower().strip()

                if med_name and (med_name in clean_q or clean_q in med_name):
                    return True, item
                if gen_name and (gen_name in clean_q or clean_q in gen_name):
                    return True, item

                med_tokens = set(re.sub(r'[^a-zA-Z0-9\s]', ' ', med_name).split()) - ignore_tokens
                if med_tokens and med_tokens.intersection(q_tokens):
                    return True, item

            # Check adverse reactions table
            conn = self.get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM medicine_reactions WHERE patient_id = ?', (patient_id,))
                reactions = cursor.fetchall()
                for r in reactions:
                    r_dict = dict(r)
                    r_med = (r_dict.get('medicine_name') or '').lower().strip()
                    if r_med and (r_med in clean_q or clean_q in r_med):
                        conn.close()
                        return True, {
                            'allergy_id': r_dict.get('reaction_id'),
                            'patient_id': patient_id,
                            'medicine_name': r_dict.get('medicine_name'),
                            'generic_name': '',
                            'severity': r_dict.get('severity', 'Moderate'),
                            'symptoms': r_dict.get('reaction_description') or str(r_dict.get('symptoms', '')),
                            'reaction_date': r_dict.get('reported_date'),
                            'notes': r_dict.get('reaction_description', 'Recorded adverse reaction')
                        }
            except Exception:
                pass
            conn.close()
            return False, None
        
        except Exception as e:
            print(f"Error checking allergy: {e}")
            return False, None
    
    # ==================== MEDICAL HISTORY ====================
    
    def add_medical_history(self, patient_id: int, disease_name: str,
                           severity: str = "Moderate", symptoms: str = "",
                           treatment: str = "", notes: str = "") -> Tuple[bool, str]:
        """Add medical history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO medical_history (
                    patient_id, disease_name, diagnosis_date, severity,
                    symptoms, treatment_given, doctor_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_id, disease_name, datetime.now(), severity,
                symptoms, treatment, notes
            ))
            
            conn.commit()
            conn.close()
            return True, "Medical history added!"
        
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def get_medical_history(self, patient_id: int) -> List[Dict]:
        """Get medical history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM medical_history 
                WHERE patient_id = ? 
                ORDER BY diagnosis_date DESC
            ''', (patient_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [dict(r) for r in results]
        
        except Exception as e:
            print(f"Error fetching history: {e}")
            return []
    
    # ==================== MEDICAL REPORTS ====================
    
    def add_report(self, patient_id: int, disease_diagnosed: str,
                  symptoms: str = "", tests: str = "", drugs: str = "",
                  precautions: str = "", llm_response: str = "",
                  confidence: float = 0.0, doctor_notes: str = "") -> Tuple[bool, str]:
        """Add medical report"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO medical_reports (
                    patient_id, disease_diagnosed, symptoms_reported,
                    tests_recommended, drugs_prescribed, precautions,
                    llm_response, confidence_score, doctor_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_id, disease_diagnosed, symptoms, tests, drugs,
                precautions, llm_response, confidence, doctor_notes
            ))
            
            report_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True, f"Report saved! ID: {report_id}"
        
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def get_reports(self, patient_id: int, limit: int = 10) -> List[Dict]:
        """Get medical reports"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM medical_reports 
                WHERE patient_id = ? 
                ORDER BY created_at DESC
                LIMIT ?
            ''', (patient_id, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            return [dict(r) for r in results]
        
        except Exception as e:
            print(f"Error fetching reports: {e}")
            return []
    
    def get_recent_report(self, patient_id: int) -> Optional[Dict]:
        """Get most recent report"""
        reports = self.get_reports(patient_id, limit=1)
        return reports[0] if reports else None
    
    # ==================== VOICE INTERACTIONS ====================
    
    def add_voice_interaction(self, patient_id: int, language: str,
                             user_text: str = "", response_text: str = "",
                             interaction_type: str = "") -> Tuple[bool, str]:
        """Log voice interaction"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO voice_interactions (
                    patient_id, language, user_input_text,
                    system_response_text, interaction_type
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                patient_id, language, user_text, response_text, interaction_type
            ))
            
            conn.commit()
            conn.close()
            return True, "Voice interaction logged!"
        
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def get_voice_history(self, patient_id: int, limit: int = 10) -> List[Dict]:
        """Get voice interaction history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM voice_interactions 
                WHERE patient_id = ? 
                ORDER BY created_at DESC
                LIMIT ?
            ''', (patient_id, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            return [dict(r) for r in results]
        
        except Exception as e:
            print(f"Error fetching voice history: {e}")
            return []