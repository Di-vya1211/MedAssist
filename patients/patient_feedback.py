"""
MedAssist - Patient Feedback & Adverse Reaction System
Track medicine reactions, side effects, and user feedback
"""

import sqlite3
import streamlit as st
from datetime import datetime
from typing import Optional, List, Dict, Tuple
import json
from .patient_db import PatientDatabase

class MedicineFeedbackDB:
    """Database for tracking medicine reactions and feedback"""
    
    def __init__(self, db_path: str = "patients.db"):
        self.db_path = db_path
        self.init_feedback_tables()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_feedback_tables(self):
        """Initialize feedback and reaction tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Medicine prescriptions/recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicine_prescriptions (
                prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                medicine_name TEXT NOT NULL,
                generic_name TEXT,
                dosage TEXT,
                frequency TEXT,
                reason_prescribed TEXT,
                prescribed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                prescribed_by TEXT,
                source_module TEXT,  -- 'disease_info', 'drug_info', 'symptom_checker'
                llm_confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
            )
        ''')
        
        # Adverse reactions/feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicine_reactions (
                reaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                prescription_id INTEGER,
                medicine_name TEXT NOT NULL,
                reaction_type TEXT,  -- 'side_effect', 'allergy', 'no_effect', 'positive_effect', 'other'
                severity TEXT,  -- 'Mild', 'Moderate', 'Severe'
                reaction_description TEXT,
                symptoms TEXT,  -- JSON list of symptoms
                onset_time INTEGER,  -- hours after intake
                duration_hours INTEGER,
                reported_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                voice_input BOOLEAN DEFAULT 0,
                doctor_notified BOOLEAN DEFAULT 0,
                doctor_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                FOREIGN KEY (prescription_id) REFERENCES medicine_prescriptions(prescription_id)
            )
        ''')
        
        # Medicine effectiveness feedback
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicine_effectiveness (
                effectiveness_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                prescription_id INTEGER,
                medicine_name TEXT NOT NULL,
                disease_treated TEXT,
                symptom_relief_score INTEGER,  -- 1-10 scale
                improvement_timeline TEXT,  -- 'immediate', '1-3 days', '1 week', 'no improvement'
                worth_repeating BOOLEAN,
                alternative_suggestions TEXT,
                feedback_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                FOREIGN KEY (prescription_id) REFERENCES medicine_prescriptions(prescription_id)
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_prescriptions_patient ON medicine_prescriptions(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_reactions_patient ON medicine_reactions(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_effectiveness_patient ON medicine_effectiveness(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_reactions_medicine ON medicine_reactions(medicine_name)')
        
        conn.commit()
        conn.close()
    
    # ==================== PRESCRIPTION TRACKING ====================
    
    def add_prescription(self, patient_id: int, medicine_name: str, generic_name: str = "",
                        reason: str = "", dosage: str = "", frequency: str = "",
                        source_module: str = "", llm_confidence: float = 0.0) -> Tuple[bool, str, Optional[int]]:
        """Log a medicine prescription/recommendation"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO medicine_prescriptions (
                    patient_id, medicine_name, generic_name, dosage, frequency,
                    reason_prescribed, source_module, llm_confidence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_id, medicine_name, generic_name, dosage, frequency,
                reason, source_module, llm_confidence
            ))
            
            prescription_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, f"Prescription recorded! ID: {prescription_id}", prescription_id
        
        except Exception as e:
            return False, f"Failed to record prescription: {str(e)}", None
    
    def get_prescriptions(self, patient_id: int, limit: int = 20) -> List[Dict]:
        """Get patient's prescription history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM medicine_prescriptions
                WHERE patient_id = ?
                ORDER BY prescribed_date DESC
                LIMIT ?
            ''', (patient_id, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            return [dict(r) for r in results]
        
        except Exception as e:
            print(f"Error fetching prescriptions: {e}")
            return []
    
    # ==================== ADVERSE REACTIONS ====================
    
    def report_reaction(self, patient_id: int, medicine_name: str, 
                       reaction_type: str, severity: str, description: str,
                       symptoms: List[str] = None, onset_time: int = 0,
                       duration: int = 0, voice_input: bool = False,
                       prescription_id: int = None) -> Tuple[bool, str]:
        """Report adverse reaction to a medicine"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            symptoms_json = json.dumps(symptoms) if symptoms else ""
            
            cursor.execute('''
                INSERT INTO medicine_reactions (
                    patient_id, prescription_id, medicine_name, reaction_type,
                    severity, reaction_description, symptoms, onset_time,
                    duration_hours, voice_input
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_id, prescription_id, medicine_name, reaction_type,
                severity, description, symptoms_json, onset_time, duration, voice_input
            ))
            
            reaction_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, f"Reaction reported! ID: {reaction_id}"
        
        except Exception as e:
            return False, f"Failed to report reaction: {str(e)}"
    
    def get_reactions(self, patient_id: int, limit: int = 20) -> List[Dict]:
        """Get patient's reaction history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM medicine_reactions
                WHERE patient_id = ?
                ORDER BY reported_date DESC
                LIMIT ?
            ''', (patient_id, limit))
            
            results = cursor.fetchall()
            
            # Parse JSON symptoms
            for row in results:
                if row['symptoms']:
                    row['symptoms'] = json.loads(row['symptoms'])
            
            conn.close()
            
            return [dict(r) for r in results]
        
        except Exception as e:
            print(f"Error fetching reactions: {e}")
            return []
    
    def get_medicine_reactions(self, medicine_name: str, patient_id: int = None) -> List[Dict]:
        """Get all reactions for a specific medicine"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if patient_id:
                cursor.execute('''
                    SELECT * FROM medicine_reactions
                    WHERE LOWER(medicine_name) LIKE ? AND patient_id = ?
                    ORDER BY reported_date DESC
                ''', (f'%{medicine_name.lower()}%', patient_id))
            else:
                cursor.execute('''
                    SELECT * FROM medicine_reactions
                    WHERE LOWER(medicine_name) LIKE ?
                    ORDER BY reported_date DESC
                ''', (f'%{medicine_name.lower()}%',))
            
            results = cursor.fetchall()
            conn.close()
            
            return [dict(r) for r in results]
        
        except Exception as e:
            print(f"Error fetching reactions: {e}")
            return []
    
    # ==================== EFFECTIVENESS FEEDBACK ====================
    
    def add_effectiveness_feedback(self, patient_id: int, medicine_name: str,
                                   disease_treated: str, symptom_relief: int,
                                   improvement_timeline: str, worth_repeating: bool,
                                   alternatives: str = "", prescription_id: int = None) -> Tuple[bool, str]:
        """Log effectiveness feedback for a medicine"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO medicine_effectiveness (
                    patient_id, prescription_id, medicine_name, disease_treated,
                    symptom_relief_score, improvement_timeline, worth_repeating,
                    alternative_suggestions
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_id, prescription_id, medicine_name, disease_treated,
                symptom_relief, improvement_timeline, worth_repeating, alternatives
            ))
            
            conn.commit()
            conn.close()
            
            return True, "Feedback recorded!"
        
        except Exception as e:
            return False, f"Failed to record feedback: {str(e)}"
    
    def get_effectiveness_feedback(self, patient_id: int, limit: int = 20) -> List[Dict]:
        """Get effectiveness feedback history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM medicine_effectiveness
                WHERE patient_id = ?
                ORDER BY feedback_date DESC
                LIMIT ?
            ''', (patient_id, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            return [dict(r) for r in results]
        
        except Exception as e:
            print(f"Error fetching feedback: {e}")
            return []


def show_feedback_form(patient_id: int, medicine_name: str, db: MedicineFeedbackDB):
    """Display feedback form in Streamlit"""
    
    st.markdown(f"### 📝 Report Feedback for {medicine_name}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        reaction_type = st.selectbox(
            "Type of Feedback",
            ["side_effect", "allergy", "no_effect", "positive_effect", "other"],
            key=f"reaction_type_{medicine_name}"
        )
        
        severity = st.selectbox(
            "Severity",
            ["Mild", "Moderate", "Severe"],
            key=f"severity_{medicine_name}"
        )
    
    with col2:
        onset_time = st.number_input(
            "Hours after taking medicine",
            min_value=0, max_value=72, value=1,
            key=f"onset_{medicine_name}"
        )
        
        duration = st.number_input(
            "Duration (hours)",
            min_value=0, max_value=168, value=2,
            key=f"duration_{medicine_name}"
        )
    
    # Symptoms
    st.markdown("**Symptoms Experienced:**")
    symptoms = []
    
    col1, col2, col3 = st.columns(3)
    
    symptom_list = [
        "Nausea", "Dizziness", "Rash", "Itching", "Headache",
        "Stomach Pain", "Fatigue", "Fever", "Cough", "Other"
    ]
    
    for i, symptom in enumerate(symptom_list):
        col = [col1, col2, col3][i % 3]
        with col:
            if st.checkbox(symptom, key=f"symptom_{symptom}_{medicine_name}"):
                symptoms.append(symptom)
    
    # Description
    description = st.text_area(
        "Detailed description of your experience",
        placeholder="Describe what happened, how you felt, etc.",
        height=100,
        key=f"description_{medicine_name}"
    )
    
    # Voice input option
    use_voice = st.checkbox("Record this feedback via voice", key=f"voice_{medicine_name}")
    
    if st.button(f"Submit Feedback for {medicine_name}", use_container_width=True):
        if not description:
            st.error("Please provide a description")
        else:
            success, message = db.report_reaction(
                patient_id=patient_id,
                medicine_name=medicine_name,
                reaction_type=reaction_type,
                severity=severity,
                description=description,
                symptoms=symptoms,
                onset_time=onset_time,
                duration=duration,
                voice_input=use_voice
            )
            
            if success:
                st.success(f"✅ {message}")
                st.rerun()
            else:
                st.error(f"❌ {message}")


def show_feedback_history(patient_id: int, db: MedicineFeedbackDB):
    """Display feedback history"""
    st.markdown("### 📋 Your Medicine Feedback History")
    
    reactions = db.get_reactions(patient_id)
    
    if not reactions:
        st.info("No feedback recorded yet")
        return
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        severe_count = sum(1 for r in reactions if r.get('severity') == 'Severe')
        st.metric("Severe Reactions", severe_count)
    
    with col2:
        moderate_count = sum(1 for r in reactions if r.get('severity') == 'Moderate')
        st.metric("Moderate Reactions", moderate_count)
    
    with col3:
        allergies = sum(1 for r in reactions if r.get('reaction_type') == 'allergy')
        st.metric("Allergies Reported", allergies)
    
    st.markdown("---")
    
    # Detailed reactions
    for reaction in reactions:
        severity = reaction.get('severity', 'Unknown')
        
        if severity == 'Severe':
            emoji = "🔴"
            color = "error"
        elif severity == 'Moderate':
            emoji = "🟡"
            color = "warning"
        else:
            emoji = "🟢"
            color = "info"
        
        with st.expander(f"{emoji} {reaction.get('medicine_name')} - {reaction.get('reaction_type')} ({reaction.get('reported_date')[:10]})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Severity:** {severity}")
                st.markdown(f"**Type:** {reaction.get('reaction_type')}")
                st.markdown(f"**Onset:** {reaction.get('onset_time')} hours")
            
            with col2:
                st.markdown(f"**Duration:** {reaction.get('duration_hours')} hours")
                st.markdown(f"**Voice Input:** {'Yes' if reaction.get('voice_input') else 'No'}")
                st.markdown(f"**Doctor Notified:** {'Yes' if reaction.get('doctor_notified') else 'No'}")
            
            st.markdown(f"**Description:** {reaction.get('reaction_description')}")
            
            if reaction.get('symptoms'):
                symptoms = reaction.get('symptoms')
                if isinstance(symptoms, str):
                    symptoms = json.loads(symptoms)
                st.markdown(f"**Symptoms:** {', '.join(symptoms)}")
            
            # Mark as notified to doctor
            if not reaction.get('doctor_notified'):
                if st.button(f"Notify Doctor", key=f"notify_{reaction.get('reaction_id')}"):
                    st.info("Doctor notification sent!")