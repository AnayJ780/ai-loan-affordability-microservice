from pydantic import BaseModel, Field , ConfigDict

class EMICalculationRequest(BaseModel):
    loan_amount: float = Field(
        ..., gt=0, le= 100_000_000, description='Principal loan amount inn INR'
    )

    annual_interest_rate: float = Field(
        ..., ge = 0 , le = 50, description = 'Annual rates in percent (0 - 50)'
    )

    tenure_months : int = Field(
        ..., gt = 12, le = 120 , description = 'Loan repayment tenure in months (12 m - 120m)'
    )

class LoanAffordabilityRequest(EMICalculationRequest):
    monthly_income: int = Field(
        ..., gt = 0, description = 'Net monthly take home amount'
    )

    existing_emi : float = Field(
         default = 0.0,  description = 'Existing monthly emi'
    )

    credit_score : int = Field(
        ..., ge = 300, le = 900, description = 'Credit Score between 300 and 900'
    )

    dependents : int = Field(
         default = 0, ge = 0, le = 10, description ='No. of financially dependents'
    
    )

    employment_years : float = Field(
        ..., gt = 0, description = 'Years employeed'
    )

class LoanAffordabilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id:int
    calcullated_emi:float
    predicted_safe_emi:float
    affordability_status:str
