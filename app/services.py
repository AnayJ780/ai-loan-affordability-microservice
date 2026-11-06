def calculate_monthly_emi(principal: float, annual_rate : float, months:int)->float:
    if annual_rate == 0:
        return round(principal/months, 2)

    monthly_rate = annual_rate/12/100

    compound_factor = (1+ monthly_rate)**months
    emi = principal * monthly_rate * compound_factor/ (compound_factor -1)

    return round(emi,2)

def evaluate_loan_affordability(monthly_income:float, existing_emi:float, calculated_emi:float)->tuple[float, str]:
    max_safe_emi = (monthly_income * 0.5) - existing_emi
    max_safe_emi = max(0.0, max_safe_emi)

    if calculated_emi <= max_safe_emi:
        status = 'APPROVED'

    elif calculated_emi <= max_safe_emi + (monthly_income *0.10):
        status = 'STRETCHED'

    else:
        status = 'HIGH RISK'

    return round(max_safe_emi, 2), status