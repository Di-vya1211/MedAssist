"""
MedAssist - Feedback Analysis & Pattern Detection
Analyze medicine reactions, compare with history, identify patterns
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import json
from .patient_feedback import MedicineFeedbackDB
from .patient_db import PatientDatabase


class FeedbackAnalyzer:
    """Analyze medicine reactions and identify patterns"""
    
    def __init__(self, db: PatientDatabase, feedback_db: MedicineFeedbackDB):
        self.db = db
        self.feedback_db = feedback_db
    
    # ==================== PATTERN ANALYSIS ====================
    
    def get_medicine_pattern(self, patient_id: int, medicine_name: str) -> Dict:
        """Analyze all reactions to a specific medicine"""
        
        reactions = self.feedback_db.get_medicine_reactions(medicine_name, patient_id)
        
        if not reactions:
            return {
                'medicine': medicine_name,
                'total_reactions': 0,
                'has_pattern': False,
                'message': "No reactions recorded for this medicine"
            }
        
        # Analyze patterns
        severity_counts = {}
        reaction_types = {}
        all_symptoms = {}
        onset_times = []
        durations = []
        
        for reaction in reactions:
            # Count severities
            severity = reaction.get('severity', 'Unknown')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # Count reaction types
            r_type = reaction.get('reaction_type', 'other')
            reaction_types[r_type] = reaction_types.get(r_type, 0) + 1
            
            # Collect symptoms
            if reaction.get('symptoms'):
                symptoms = reaction.get('symptoms')
                if isinstance(symptoms, str):
                    symptoms = json.loads(symptoms)
                for symptom in symptoms:
                    all_symptoms[symptom] = all_symptoms.get(symptom, 0) + 1
            
            # Collect onset times and durations
            if reaction.get('onset_time'):
                onset_times.append(reaction.get('onset_time'))
            if reaction.get('duration_hours'):
                durations.append(reaction.get('duration_hours'))
        
        # Calculate averages
        avg_onset = sum(onset_times) / len(onset_times) if onset_times else 0
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Find most common symptom
        most_common_symptom = max(all_symptoms, key=all_symptoms.get) if all_symptoms else None
        
        # Determine if there's a pattern
        has_pattern = len(reactions) >= 2 and (
            any(count >= 2 for count in severity_counts.values()) or
            any(count >= 2 for count in reaction_types.values()) or
            any(count >= 2 for count in all_symptoms.values())
        )
        
        return {
            'medicine': medicine_name,
            'total_reactions': len(reactions),
            'has_pattern': has_pattern,
            'severity_breakdown': severity_counts,
            'reaction_types': reaction_types,
            'common_symptoms': all_symptoms,
            'most_common_symptom': most_common_symptom,
            'avg_onset_hours': avg_onset,
            'avg_duration_hours': avg_duration,
            'reactions': reactions
        }
    
    # ==================== CROSS-MEDICINE ANALYSIS ====================
    
    def compare_old_medicine_with_new_symptoms(self, patient_id: int, 
                                              old_medicine: str, 
                                              new_symptoms: List[str]) -> Dict:
        """
        Compare old medicine reactions with new symptoms
        to see if there's a connection
        """
        
        # Get reactions to old medicine
        old_reactions = self.feedback_db.get_medicine_reactions(old_medicine, patient_id)
        
        if not old_reactions:
            return {
                'old_medicine': old_medicine,
                'new_symptoms': new_symptoms,
                'connection_probability': 0.0,
                'message': f"No prior reactions recorded for {old_medicine}",
                'recommendation': "No historical data to compare"
            }
        
        # Extract symptoms from old reactions
        old_symptoms_set = set()
        for reaction in old_reactions:
            if reaction.get('symptoms'):
                symptoms = reaction.get('symptoms')
                if isinstance(symptoms, str):
                    symptoms = json.loads(symptoms)
                old_symptoms_set.update(symptoms)
        
        # Find overlap
        new_symptoms_set = set(new_symptoms)
        overlap = old_symptoms_set.intersection(new_symptoms_set)
        
        # Calculate probability
        if len(new_symptoms_set) > 0:
            overlap_percentage = (len(overlap) / len(new_symptoms_set)) * 100
        else:
            overlap_percentage = 0
        
        # Generate recommendation
        if len(overlap) >= 1:
            probability = "HIGH"
            recommendation = f"⚠️ The medicine {old_medicine} previously caused similar symptoms: {', '.join(overlap)}. AVOID this medicine."
        elif overlap_percentage >= 50:
            probability = "MEDIUM"
            recommendation = f"⚡ Some overlap with previous reactions to {old_medicine}. Use caution."
        else:
            probability = "LOW"
            recommendation = f"Different symptoms from previous reactions. Likely unrelated."
        
        return {
            'old_medicine': old_medicine,
            'new_symptoms': new_symptoms,
            'previous_symptoms': list(old_symptoms_set),
            'overlapping_symptoms': list(overlap),
            'overlap_percentage': overlap_percentage,
            'connection_probability': probability,
            'recommendation': recommendation,
            'old_reaction_count': len(old_reactions),
            'old_reactions': old_reactions
        }
    
    # ==================== DISEASE-MEDICINE-REACTION ANALYSIS ====================
    
    def analyze_disease_medicine_reaction_chain(self, patient_id: int,
                                               disease_name: str,
                                               prescribed_medicine: str,
                                               new_symptoms: List[str]) -> Dict:
        """
        Full chain analysis:
        Disease → Prescribed Medicine → Reaction/Side Effect
        """
        
        # Get patient's history
        patient = self.db.get_patient(patient_id)
        medical_history = self.db.get_medical_history(patient_id)
        allergies = self.db.get_allergies(patient_id)
        
        # Check if disease is in history
        disease_history = [h for h in medical_history if disease_name.lower() in h.get('disease_name', '').lower()]
        
        # Check if patient has allergy to medicine
        is_allergic, allergy_data = self.db.check_drug_allergy(patient_id, prescribed_medicine)
        
        # Get reactions to this medicine
        medicine_reactions = self.feedback_db.get_medicine_reactions(prescribed_medicine, patient_id)
        
        # Build analysis
        analysis = {
            'disease': disease_name,
            'medicine': prescribed_medicine,
            'new_symptoms': new_symptoms,
            'patient_name': patient.get('full_name') if patient else 'Unknown',
            'patient_age': patient.get('age') if patient else 'Unknown',
            'blood_type': patient.get('blood_type') if patient else 'Unknown',
            'disease_history': disease_history,
            'has_prior_allergy': is_allergic,
            'allergy_data': allergy_data,
            'prior_reactions_to_medicine': len(medicine_reactions),
            'medicine_reactions': medicine_reactions,
            'conclusion': self._generate_conclusion(disease_name, prescribed_medicine, is_allergic, 
                                                   disease_history, medicine_reactions, new_symptoms),
            'recommendations': self._generate_recommendations(is_allergic, medicine_reactions, new_symptoms)
        }
        
        return analysis
    
    # ==================== CONCLUSION GENERATION ====================
    
    def _generate_conclusion(self, disease: str, medicine: str, is_allergic: bool,
                            disease_history: List, medicine_reactions: List,
                            new_symptoms: List) -> str:
        """Generate conclusion from all available data"""
        
        conclusions = []
        
        # Allergy check
        if is_allergic:
            conclusions.append(f"⚠️ CRITICAL: Patient has documented allergy to {medicine}!")
        
        # Prior reaction check
        if medicine_reactions:
            conclusions.append(f"⚠️ Patient previously had {len(medicine_reactions)} reaction(s) to {medicine}!")
        
        # Disease history check
        if disease_history:
            conclusions.append(f"ℹ️ Patient has history of {disease} ({len(disease_history)} occurrence(s))")
        
        # New symptoms analysis
        if new_symptoms:
            conclusions.append(f"🔴 New symptoms reported: {', '.join(new_symptoms)}")
        
        # Final verdict
        if is_allergic or (medicine_reactions and len(medicine_reactions) >= 2):
            conclusions.append("❌ **RECOMMENDATION: AVOID THIS MEDICINE**")
        elif medicine_reactions:
            conclusions.append("⚠️ **RECOMMENDATION: USE WITH CAUTION - MONITOR CLOSELY**")
        else:
            conclusions.append("✅ **RECOMMENDATION: SAFE TO USE - NO PRIOR ISSUES**")
        
        return "\n".join(conclusions)
    
    def _generate_recommendations(self, is_allergic: bool, reactions: List, new_symptoms: List) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        if is_allergic:
            recommendations.append("❌ DO NOT USE - Patient is allergic")
            recommendations.append("🔄 Ask doctor for alternative medicine")
        
        if reactions and len(reactions) >= 1:
            recommendations.append("⚠️ Monitor for adverse reactions")
            recommendations.append("📞 Contact doctor if symptoms worsen")
        
        if new_symptoms:
            recommendations.append(f"📋 Log symptoms: {', '.join(new_symptoms)}")
            recommendations.append("📱 Share this information with your doctor")
        
        if not is_allergic and not reactions:
            recommendations.append("✅ No prior issues - Safe to use")
            recommendations.append("📝 Note any reactions for future reference")
        
        return recommendations


def show_analysis_page(patient_id: int, db: PatientDatabase, feedback_db: MedicineFeedbackDB):
    """Display comprehensive analysis page"""
    
    analyzer = FeedbackAnalyzer(db, feedback_db)
    
    st.markdown("### 🔍 Medicine Reaction Analysis")
    
    # Get patient's medicines
    prescriptions = feedback_db.get_prescriptions(patient_id)
    medicine_list = list(set([p.get('medicine_name') for p in prescriptions]))
    
    if not medicine_list:
        st.info("No medicines in your history")
        return
    
    # Select medicine to analyze
    selected_medicine = st.selectbox("Select medicine to analyze", medicine_list)
    
    if selected_medicine:
        # Get pattern for selected medicine
        pattern = analyzer.get_medicine_pattern(patient_id, selected_medicine)
        
        if pattern['has_pattern']:
            st.warning(f"⚠️ Pattern detected for {selected_medicine}")
        else:
            st.info(f"ℹ️ Analyzing {selected_medicine}...")
        
        # Display pattern analysis
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Reactions", pattern.get('total_reactions', 0))
        
        with col2:
            most_common = pattern.get('most_common_symptom', 'None')
            st.metric("Most Common Symptom", most_common)
        
        with col3:
            st.metric("Avg Onset (hrs)", f"{pattern.get('avg_onset_hours', 0):.1f}")
        
        # Detailed breakdown
        if pattern.get('has_pattern'):
            st.markdown("---")
            st.markdown("**Severity Breakdown:**")
            for severity, count in pattern.get('severity_breakdown', {}).items():
                st.text(f"{severity}: {count} occurrence(s)")
            
            st.markdown("**Common Symptoms:**")
            for symptom, count in sorted(pattern.get('common_symptoms', {}).items(), 
                                        key=lambda x: x[1], reverse=True)[:5]:
                st.text(f"{symptom}: {count} time(s)")


def show_comparison_analysis(patient_id: int, db: PatientDatabase, feedback_db: MedicineFeedbackDB):
    """Show comparison analysis between medicines"""
    
    analyzer = FeedbackAnalyzer(db, feedback_db)
    
    st.markdown("### 🔄 Compare Old Medicine with New Symptoms")
    
    prescriptions = feedback_db.get_prescriptions(patient_id)
    medicine_list = list(set([p.get('medicine_name') for p in prescriptions]))
    
    if not medicine_list:
        st.info("No medicines to compare")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        old_medicine = st.selectbox("Medicine you used before", medicine_list, key="old_med")
    
    with col2:
        new_symptoms = st.multiselect("New symptoms you're experiencing", [
            "Nausea", "Dizziness", "Rash", "Itching", "Headache",
            "Stomach Pain", "Fatigue", "Fever", "Cough"
        ], key="new_sym")
    
    if old_medicine and new_symptoms:
        if st.button("Analyze Connection"):
            comparison = analyzer.compare_old_medicine_with_new_symptoms(
                patient_id, old_medicine, new_symptoms
            )
            
            # Display results
            st.markdown(f"### Analysis: {old_medicine}")
            
            st.info(comparison['recommendation'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Previous Symptoms:**")
                for symptom in comparison.get('previous_symptoms', []):
                    st.text(f"• {symptom}")
            
            with col2:
                st.markdown("**Overlapping Symptoms:**")
                for symptom in comparison.get('overlapping_symptoms', []):
                    st.error(f"🔴 {symptom}")
            
            st.markdown(f"**Overlap Percentage:** {comparison.get('overlap_percentage', 0):.1f}%")
            st.markdown(f"**Connection Probability:** {comparison.get('connection_probability')}")


def show_full_chain_analysis(patient_id: int, db: PatientDatabase, feedback_db: MedicineFeedbackDB):
    """Show disease → medicine → reaction analysis"""
    
    analyzer = FeedbackAnalyzer(db, feedback_db)
    
    st.markdown("### 📊 Full Disease-Medicine-Reaction Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        disease = st.text_input("Disease/Condition:", placeholder="e.g., Diabetes, Asthma")
        medicine = st.text_input("Medicine prescribed:", placeholder="e.g., Metformin")
    
    with col2:
        symptoms = st.multiselect("Symptoms you experienced:", [
            "Nausea", "Dizziness", "Rash", "Itching", "Headache",
            "Stomach Pain", "Fatigue", "Fever", "Cough", "Other"
        ])
    
    if disease and medicine and symptoms:
        if st.button("Analyze Full Chain"):
            analysis = analyzer.analyze_disease_medicine_reaction_chain(
                patient_id, disease, medicine, symptoms
            )
            
            # Display comprehensive analysis
            st.markdown(f"### Analysis Report")
            st.markdown(f"**Disease:** {analysis['disease']}")
            st.markdown(f"**Medicine:** {analysis['medicine']}")
            st.markdown(f"**Patient:** {analysis['patient_name']} (Age: {analysis['patient_age']}, Blood Type: {analysis['blood_type']})")
            
            st.markdown("---")
            
            # Conclusion
            st.markdown("### 🎯 Conclusion")
            st.markdown(analysis['conclusion'])
            
            # Recommendations
            st.markdown("### 💊 Recommendations")
            for i, rec in enumerate(analysis['recommendations'], 1):
                st.markdown(f"{i}. {rec}")
            
            # Details
            with st.expander("📋 Detailed Analysis"):
                if analysis['disease_history']:
                    st.markdown(f"**Disease History:** {len(analysis['disease_history'])} occurrence(s)")
                
                if analysis['has_prior_allergy']:
                    st.error(f"⚠️ ALLERGY ALERT: {analysis['allergy_data'].get('severity')} allergy to {medicine}")
                
                st.markdown(f"**Prior Reactions to {medicine}:** {analysis['prior_reactions_to_medicine']}")