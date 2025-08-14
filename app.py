#!/usr/bin/env python3
"""
Learning Plan Generator - Streamlit Web UI
A modern web interface for the AI-powered learning plan generator
"""

import streamlit as st
import json
import os
from typing import Dict, Any
import time

from models import UserInput, LearningFormat
from workflow import LearningPlanWorkflow
from config import GOOGLE_API_KEY

# Page configuration
st.set_page_config(
    page_title="Learning Plan Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .plan-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .success-metric {
        background: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
    }
    .resource-item {
        background: #e2e3e5;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

def check_api_key():
    """Check if API key is available"""
    if not GOOGLE_API_KEY:
        st.error("❌ GOOGLE_API_KEY not found in environment variables.")
        st.info("Please set your Gemini API key in the .env file or as an environment variable.")
        st.markdown("""
        **To set up:**
        1. Create a .env file in the project directory
        2. Add: `GOOGLE_API_KEY=your_actual_api_key_here`
        3. Get your API key from: [Google AI Studio](https://makersuite.google.com/app/apikey)
        """)
        return False
    return True

def display_learning_plan(plan: Dict[str, Any]):
    """Display the complete learning plan in a beautiful format"""
    
    # User Input Summary
    st.markdown("### 📋 Learning Plan Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Topic", plan['user_input']['topic'])
    with col2:
        st.metric("Format", plan['user_input']['preferred_format'].title())
    with col3:
        st.metric("Background", plan['user_input']['background'][:30] + "..." if len(plan['user_input']['background']) > 30 else plan['user_input']['background'])
    
    # Knowledge Gap Analysis
    st.markdown("### 🔍 Knowledge Gap Analysis")
    gap = plan['knowledge_gap']
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Current Level:** {gap['current_level']}")
        st.info(f"**Target Level:** {gap['target_level']}")
    
    with col2:
        st.warning(f"**Identified Gaps:** {', '.join(gap['identified_gaps'])}")
    
    st.markdown(f"**Analysis:** {gap['gap_analysis']}")
    
    # Topic Plan
    st.markdown("### 📚 Topic Plan")
    topic_plan = plan['topic_plan']
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Main Topics:**")
        for topic in topic_plan['main_topics']:
            st.markdown(f"• {topic}")
    
    with col2:
        st.markdown("**Learning Objectives:**")
        for objective in topic_plan['learning_objectives']:
            st.markdown(f"• {objective}")
    
    st.info(f"**Estimated Duration:** {topic_plan['estimated_duration']}")
    
    # Topic Details
    st.markdown("### 📝 Detailed Topic Breakdown")
    
    for i, detail in enumerate(plan['topic_details'], 1):
        with st.expander(f"{i}. {detail['topic_name']}", expanded=False):
            st.markdown(f"**Description:** {detail['description']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Resources:**")
                for resource in detail['resources']:
                    st.markdown(f"• {resource}")
            
            with col2:
                st.markdown("**Exercises:**")
                for exercise in detail['exercises']:
                    st.markdown(f"• {exercise}")
            
            st.markdown(f"**Assessment:** {detail['assessment_criteria']}")
    
    # Combined Plan
    st.markdown("### 🔗 Complete Learning Path")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Learning Path:** {plan['learning_path']}")
        st.markdown(f"**Timeline:** {plan['timeline']}")
    
    with col2:
        st.markdown("**Success Metrics:**")
        for metric in plan['success_metrics']:
            st.markdown(f"<div class='success-metric'>✓ {metric}</div>", unsafe_allow_html=True)
    
    st.markdown("**Overall Resources:**")
    for resource in plan['recommended_resources']:
        st.markdown(f"<div class='resource-item'>📚 {resource}</div>", unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Learning Plan Generator</h1>
        <p>AI-powered personalized learning plans using LangChain and Gemini</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    if not check_api_key():
        st.stop()
    
    # Sidebar for navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.radio("Choose a page:", ["Generate Plan", "About", "Settings"])
    
    if page == "Generate Plan":
        st.markdown("## 🚀 Create Your Learning Plan")
        
        # User input form
        with st.form("learning_plan_form"):
            st.markdown("### 📚 What would you like to learn?")
            
            topic = st.text_input(
                "Topic",
                placeholder="e.g., Machine Learning, Python Programming, Data Science...",
                help="Enter the topic you want to learn"
            )
            
            background = st.text_area(
                "Your Background & Experience",
                placeholder="e.g., I'm a beginner with no programming experience, or I have intermediate Python skills...",
                help="Describe your current knowledge level and experience"
            )
            
            preferred_format = st.selectbox(
                "Preferred Learning Format",
                options=["video", "text", "audio"],
                format_func=lambda x: x.title(),
                help="Choose how you prefer to consume learning content"
            )
            
            submitted = st.form_submit_button("🚀 Generate Learning Plan", use_container_width=True)
        
        if submitted:
            # Validate inputs
            if not topic or not background:
                st.error("❌ Please fill in all required fields.")
                st.stop()
            
            # Create user input
            user_input = UserInput(
                topic=topic,
                background=background,
                preferred_format=LearningFormat(preferred_format),
                max_iterations=1
            )
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Initialize workflow
                status_text.text("🚀 Initializing AI workflow...")
                progress_bar.progress(25)
                time.sleep(1)
                
                workflow = LearningPlanWorkflow()
                
                # Create learning plan
                status_text.text("🧠 Analyzing your knowledge gaps...")
                progress_bar.progress(50)
                time.sleep(1)
                
                status_text.text("📚 Planning your learning path...")
                progress_bar.progress(75)
                time.sleep(1)
                
                status_text.text("🔗 Combining everything into your plan...")
                progress_bar.progress(90)
                
                learning_plan = workflow.create_learning_plan(user_input)
                
                progress_bar.progress(100)
                status_text.text("✅ Learning plan generated successfully!")
                time.sleep(1)
                
                # Display the plan
                st.success("🎉 Your personalized learning plan is ready!")
                display_learning_plan(learning_plan.model_dump())
                
                # Download option
                plan_json = json.dumps(learning_plan.model_dump(), indent=2)
                filename = f"learning_plan_{topic.replace(' ', '_').lower()}.json"
                
                st.download_button(
                    label="💾 Download Plan as JSON",
                    data=plan_json,
                    file_name=filename,
                    mime="application/json",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("Please check your API key and try again.")
    
    elif page == "About":
        st.markdown("## 📖 About Learning Plan Generator")
        
        st.markdown("""
        This application uses advanced AI agents to create personalized learning plans:
        
        ### 🤖 AI Agents
        - **Gap Analysis Agent**: Analyzes your current knowledge and identifies gaps
        - **Topic Planning Agent**: Creates a structured learning path
        - **Topic Detail Agent**: Provides detailed breakdowns and resources
        - **Plan Combiner Agent**: Combines everything into a cohesive plan
        
        ### 🛠️ Technology Stack
        - **LangChain**: AI application framework
        - **LangGraph**: Workflow orchestration
        - **Google Gemini**: Advanced AI model
        - **Streamlit**: Modern web interface
        
        ### 🎯 Features
        - Personalized learning paths
        - Multiple learning format support
        - Detailed resource recommendations
        - Progress tracking metrics
        - Exportable learning plans
        """)
        
        st.info("💡 **Tip**: The more detailed you are about your background, the better your learning plan will be!")
    
    elif page == "Settings":
        st.markdown("## ⚙️ Settings")
        
        st.markdown("### 🔑 API Configuration")
        if GOOGLE_API_KEY:
            st.success("✅ Google Gemini API key is configured")
            # Show masked API key
            masked_key = "*" * (len(GOOGLE_API_KEY) - 4) + GOOGLE_API_KEY[-4:] if len(GOOGLE_API_KEY) > 4 else "*" * len(GOOGLE_API_KEY)
            st.code(f"API Key: {masked_key}")
        else:
            st.error("❌ Google Gemini API key not found")
        
        st.markdown("### 📁 Environment")
        st.code(f"Project Directory: {os.getcwd()}")
        st.code(f"Python Version: {os.sys.version}")
        
        st.markdown("### 🔧 Configuration")
        from config import MODEL_NAME, TEMPERATURE, MAX_TOKENS
        st.code(f"Model: {MODEL_NAME}")
        st.code(f"Temperature: {TEMPERATURE}")
        st.code(f"Max Tokens: {MAX_TOKENS}")

if __name__ == "__main__":
    main() 