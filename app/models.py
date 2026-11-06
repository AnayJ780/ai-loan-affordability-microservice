from datetime import datetime, timezone
from sqlalchemy import String , Float , Integer , DateTime
from sqlalchemy.orm import Mapped , mapped_column
from database import Base

class LoanApplication(Base):
    __tablename__ = 'loan_applications'

    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    monthly_income: Mapped[float] = mapped_column(Float, nullable = False)
    existing_emi: Mapped[float] = mapped_column(Float, nullable = False)
    credit_score: Mapped[int] = mapped_column(Integer, nullable = False)
    dependents: Mapped[int] = mapped_column(Integer, nullable = False)
    employment_years: Mapped[float] = mapped_column(Float, nullable=False, default = 0)

    loan_amount : Mapped[float] = mapped_column(Float , nullable = False)
    annual_interest_rate: Mapped[float] = mapped_column(Float, nullable = False)
    tenure_months: Mapped[int] = mapped_column(Integer, nullable = False)

    calculated_emi: Mapped[float] = mapped_column(Float, nullable = False)
    predicted_max_safe_emi: Mapped[float] = mapped_column(Float, nullable = False)
    affordability_status: Mapped[str] = mapped_column(String(30), nullable = False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone = True), default = lambda: datetime.now(timezone.utc), nullable = False)