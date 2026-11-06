import os
import logging
import pandas as pd
import joblib
from google import genai
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
load_dotenv()
# 1. IMPORT YOUR MODULAR FILES
from database import engine, get_db
import models
import schemas
import services

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("LoanAPI")
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Loan Affordability Analyzer")

# CORS Middleware for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Scikit-Learn Model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "models", "loan_model.joblib")
model = joblib.load(model_path)

# Configure the modern Gemini Client
client = genai.Client(api_key="your_api_key")

# 2. THE ENDPOINT
@app.post("/predict")
def predict_emi(request: schemas.LoanAffordabilityRequest, db: Session = Depends(get_db)):
    try:
        # A. Do the Math (Using your services.py)
        calc_emi = services.calculate_monthly_emi(
            request.loan_amount, request.annual_interest_rate, request.tenure_months
        )

        # B. ML Prediction
        # Extract only the 5 features the ML model expects
        ml_input = pd.DataFrame([{
            "monthly_income": request.monthly_income,
            "existing_emi": request.existing_emi,
            "credit_score": request.credit_score,
            "dependents": request.dependents,
            "employment_years": request.employment_years
        }])
        raw_prediction = model.predict(ml_input)[0]
        max_safe_emi = round(float(raw_prediction), 2)

        # C. Affordability Status (Using your services.py)
        _, status = services.evaluate_loan_affordability(
            request.monthly_income, request.existing_emi, calc_emi
        )

        # D. Gemini Analysis
        # D. Gemini Analysis (Upgraded Prompt)
        prompt = f"""
        Act as a strict, expert AI Loan Officer. 
        A borrower with a monthly income of ₹{request.monthly_income}, an existing EMI of ₹{request.existing_emi}, and a credit score of {request.credit_score} is requesting a loan of ₹{request.loan_amount}.
        This will result in a new EMI of ₹{calc_emi}. 
        The ML risk model evaluated this and assigned a status of '{status}' (Max safe EMI is calculated at ₹{max_safe_emi}).
        
        Write a 3-sentence professional response directly to the borrower:
        1. Explain what their '{status}' rating means using their specific numbers.
        2. If the status is 'HIGH RISK' or 'STRETCHED', explicitly advise them NOT to take this exact loan because it will cause financial distress. If 'APPROVED', confirm it is safe.
        3. Give one highly specific, actionable financial suggestion (e.g., request a lower amount, increase the loan tenure to X months, or pay off the existing EMI first).
        """
        ai_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        explanation = ai_response.text.strip()

        # E. Save to Database
        new_record = models.LoanApplication(
            monthly_income=request.monthly_income,
            existing_emi=request.existing_emi,
            credit_score=request.credit_score,
            dependents=request.dependents,
            employment_years=request.employment_years,
            loan_amount=request.loan_amount,
            annual_interest_rate=request.annual_interest_rate,
            tenure_months=request.tenure_months,
            calculated_emi=calc_emi,
            predicted_max_safe_emi=max_safe_emi,
            affordability_status=status
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)

        # F. Return to Streamlit
        return {
            "predicted_approved_emi": max_safe_emi,
            "calculated_emi": calc_emi,
            "status": status,
            "ai_explanation": explanation
        }
    except Exception as e:
        logger.error(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))