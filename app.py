import streamlit as st
import pandas as pd
import time
import os
import sys

# --- 1. SETUP: ENSURING CREWAI IMPORTS WORK ---
# This path modification allows Streamlit (running in the root) to find the 'finance' package.
# Assuming 'finance' directory contains crew.py
if os.path.abspath(os.path.join(os.getcwd(), 'finance')) not in sys.path:
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'finance')))

try:
    # Attempt the import now that the path is set
    from src.finance.crew import Finance
except ImportError as e:
    st.error(f"Error importing Finance Crew. Make sure the 'finance' package (containing crew.py) is set up correctly.")
    st.stop()

# --- 2. ENVIRONMENT AND CONFIGURATION ---
# for streamlit deployment you can set them in the secrets section
def load_secrets():
    """Loads API keys from Streamlit secrets into the os.environ for CrewAI/litellm compatibility."""
    
    # Add CHROMA_OPENAI_API_KEY to the required keys list
    required_keys = ["OPENAI_API_KEY", "AV_API_KEY", "GOOGLE_API_KEY", "SERPER_API_KEY"] 
    
    for key in required_keys:
        if key in st.secrets:
            # Set the key from Streamlit secrets
            os.environ[key] = st.secrets[key]
        elif not os.getenv(key):
            st.warning(f"⚠️ Warning: {key} is missing. Crew execution may fail.")

    # CRITICAL FIX: Ensure CHROMA_OPENAI_API_KEY is set to the same value
    if os.environ.get("OPENAI_API_KEY"):
        os.environ["CHROMA_OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"] # <--- ADD THIS LINE
    else:
        st.warning("⚠️ Warning: CHROMA_OPENAI_API_KEY is not set.")

# Load the keys immediately at app startup
load_secrets()

# FOR LOCAL FILES OS ENVIRONMENT VARIABLES
from dotenv import load_dotenv
load_dotenv() 
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["AV_API_KEY"] = os.getenv("AV_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

st.set_page_config(
    page_title="Dynamic Financial Strategy Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. CREW EXECUTION FUNCTION ---

def run_financial_crew(capital: int, timeline: int, risk: int, preferences: str,investement_strategy:str):
    """Formats the prompt and executes the CrewAI workflow."""
    
    
    prompt = f"""
    the capital that I want to invest {capital:,.0f} dollars using {investement_strategy}. 
    My primary investment goal is for the next {timeline} years. 
    I am looking for a diversified portfolio with a mix of growth and value and dividend stocks. 
    I am particularly interested in {preferences}. 
    My risk is (score {risk}/10).
    
    Specific asset preferences: {preferences}
    
    Please provide a detailed investment strategy, including specific stock recommendations, allocation percentages, 
    and rationale for each choice, integrated into the final report.
    """
    
    inputs = {'goal': prompt}
    
    # Execute the crew and capture the final markdown output
    try:
        crew = Finance().crew()
        result = crew.kickoff(inputs=inputs)
        return result
    except Exception as e:
        st.error(f"Crew Execution Failed: {e}")
        return None

# --- 4. STREAMLIT UI LAYOUT ---

st.title("💰 Dynamic Financial Strategy Generator")
st.markdown("---")

st.header("1. Client Intake Parameters")
st.caption("Customize the inputs below to generate a new, dynamically tailored investment strategy.")

with st.form("client_intake_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        initial_capital = st.number_input(
            "Initial Capital ($USD)", 
            min_value=10000, 
            max_value=10000000, 
            value=1000000,
            step=100000,
            format="%d",
            help="Total amount of capital to be strategically allocated."
        )
        
        timeline_years = st.slider(
            "Investment Timeline (Years)", 
            min_value=1, 
            max_value=30, 
            value=15, # years
            step=1,
            help="The client's long-term horizon for this investment."
        )

    with col2:
        risk_tolerance = st.slider(
            "Verified Risk Tolerance Score (1=Low, 10=High)", 
            min_value=1, 
            max_value=10, 
            value=7, 
            step=1,
            help="The dynamic risk score used by the agents to determine strategy (Growth vs. Preservation)."
        )
        
        sector_preferences = st.text_area(
            "Specific Investment Preferences",
            value="Technology, AI, Semiconductors, Dividend stocks, broad-market ETFs.",
            height=100,
            help="This raw text informs sector selection and allocation compliance."
        )
        investement_strategy=st.selectbox(
            "Investment Strategy",
            options=["Dolar Cost Averging","Growth Investing"],
            index=0,
            help="Choose the investment strategy that best fits your goals."
        )

    
    submitted = st.form_submit_button("Generate Investment Strategy (Run Crew)")

# --- 5. RESULTS DISPLAY ---

if submitted:
    st.markdown("---")
    st.header("2. Crew Execution Status")
    
    # Use a spinner to show the crew is working
    with st.spinner("🚀 Running the 6-step financial crew (Client Profiling to Final Report)... This may take a minute or two."):
        final_report_markdown = run_financial_crew(
            int(initial_capital), int(timeline_years), risk_tolerance, sector_preferences,investement_strategy
        )

    if final_report_markdown:
        st.success("✅ Analysis Complete! Final Investment Recommendation is ready.")
        st.subheader("Final Investment Recommendation Report")
        
        # Display the output directly as Markdown
        st.markdown(final_report_markdown)
    else:
        st.error("❌ Crew execution failed. Check the terminal logs for specific errors.")
