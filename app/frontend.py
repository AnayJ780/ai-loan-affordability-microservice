import streamlit as st
import requests

st.title("AI Loan Affordability Analyzer")
st.write("Enter the borrower's details below to calculate their maximum approved EMI.")

# UI Input Fields
monthly_income = st.number_input("Monthly Income(₹)", min_value=0.0, value=100000.0, step=5000.0)
existing_emi = st.number_input("Existing EMI(₹)", min_value=0.0, value=10000.0, step=1000.0)
credit_score = st.number_input("Credit Score", min_value=300, max_value=900, value=750, step=10)
dependents = st.number_input("Number of Dependents", min_value=0, value=0, step=1)
employment_years = st.number_input("Years of Employment", min_value=0.0, value=5.0, step=0.5)
loan_amount = st.number_input("Requested Loan Amount (₹)", min_value=1000.0, value=500000.0)
annual_interest_rate = st.number_input("Annual Interest Rate (%)", min_value=1.0, value=10.5)
tenure_months = st.number_input("Loan Tenure (Months)", min_value=12, value=60)

if st.button("Calculate Approved EMI"):
    
    payload = {
        "monthly_income": monthly_income,
        "existing_emi": existing_emi,
        "credit_score": credit_score,
        "dependents": dependents,
        "employment_years": employment_years,
        "loan_amount": loan_amount,
        "annual_interest_rate": annual_interest_rate,
        "tenure_months": tenure_months

    }
    
    with st.spinner(" AI Loan Officer is analyzing the profile..."):
        try:
            # THE FIX: Added timeout=10
            response = requests.post("http://localhost:8000/predict", json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                final_emi = result["predicted_approved_emi"]
                ai_insight = result["ai_explanation"]
                
                st.success("Analysis Complete!")
                
                st.metric(label="Maximum Approved EMI", value=f"₹ {final_emi:,.2f}")
                st.info(f"🏦 **AI Loan Officer Insight:**\n\n{ai_insight}")
                
            else:
                st.error(f"Backend Error: {response.text}")
                
        except requests.exceptions.Timeout:
            st.error("⏱️ Timeout Error: FastAPI took longer than 10 seconds to respond. Check the FastAPI terminal for Gemini API errors.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection Error: Is your FastAPI backend running on port 8000?")